from django.shortcuts import render,redirect
# from .models import ideas,iSummary
from .models import ideas, iSummary, Feedback, ProfaneIdeas
from better_profanity import profanity

# from .forms import ideaForm, feedbackForm
from .forms import ideaForm
from django.db.models import Prefetch

# Start idea concatenate
import mysql.connector
from django.db import connection
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin_min
from collections import Counter
from django.conf import settings
from django.shortcuts import render
from .models import iSummary

from django.http import JsonResponse
from django.shortcuts import render
from .models import iSummary

def get_summaries(request, town):
    summaries = iSummary.objects.filter(town=town, isActive=True).values('area', 'Summary')
    data = {}
    for summary in summaries:
        if summary['area'] not in data:
            data[summary['area']] = []
        data[summary['area']].append(summary['Summary'])
    print(data)
    return JsonResponse(data)

def display_ideas(request):
    towns = ['Southbury', 'Middlebury', 'Woodbury']  # List of towns
    context = {
        'towns': towns,
    }
    return render(request, 'idea_list.html', context)


"""
town_area_combinations = [
('Southbury','Park & Recreation'),
('Southbury','School'),
('Southbury','Library'),
('Southbury','Senior Center'),
('Southbury','Shopping/Stores'),
('Southbury','Police Dept'),
('Southbury','Fire Dept'),
('Southbury','Medical'),
('Southbury','Tax Collector'),
('Southbury','Restaurants'),
('Southbury','Environment'),
('Southbury','Others'),
('Middlebury','Park & Recreation'),
('Middlebury','School'),
('Middlebury','Library'),
('Middlebury','Senior Center'),
('Middlebury','Shopping/Stores'),
('Middlebury','Police Dept'),
('Middlebury','Fire Dept'),
('Middlebury','Medical'),
('Middlebury','Tax Collector'),
('Middlebury','Restaurants'),
('Middlebury','Environment'),
('Middlebury','Others')]
valid_towns = ['Southbury', 'Middlebury']
valid_area = ['Park & Recreation', 'School','Library','Senior Center','Shopping/Stores','Police Dept',
'Fire Dept','Medical','Tax Collector','Restaurants','Environment','Others']
"""

from django.http import JsonResponse

def disclaimer_seen(request):
    request.session["disclaimer_seen"] = True
    return JsonResponse({"status": "success"})

# Start Summary code
def gen_sim_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)

def generate_summary(ideas, top_n=3):
    stop_words = stopwords.words('english')
    sentences = ideas
    sentences=[s.idea.strip() for s in ideas]
    sentences = [s for s in sentences if len(s)>0 and s not in stop_words]

    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)

    num_clusters = min(len(sentences), 3)
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    cluster_sentences = [[] for _ in range(num_clusters)]
    for i, label in enumerate(kmeans.labels_):
        cluster_sentences[label].append(sentences[i])

    cluster_counts = [Counter(cluster) for cluster in cluster_sentences]

    # print(cluster_sentences)
    selected_sentences = []
    for cluster_count, cluster in zip(cluster_counts, cluster_sentences):
        selected_cluster = max(cluster_count, key=lambda x: cluster_count[x])
        selected_sentences.append(selected_cluster)

    return "* ".join(selected_sentences[:top_n])
    

# End Summary code


# def load_summary_sections():
   
#     summary_sections = []
#     for town, area in town_area_combinations:
#         summary_queryset = iSummary.objects.filter(town=town, area=area, isActive=True)
#         summary_sections.append(summary_queryset)
#     # return render(request, 'summary_template.html', {'summary_sections': summary_sections})
#     if summary_sections==[]:
#         # Need to check when this section executes
#         return summary_sections
#     else:
#         return summary_sections
    
# Modify this function to use settings
def load_summary_sections():
    summary_sections = []
    for town, area in settings.TOWN_AREA_COMBINATIONS:
        summary_queryset = iSummary.objects.filter(town=town, area=area, isActive=True)
        summary_sections.append(summary_queryset)
    return summary_sections if summary_sections else []




from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from .models import UserProfile

def home(request):
    session_key = request.session.session_key
    if not session_key:
        # Create a new session if one doesn't exist
        request.session.create()
        session_key = request.session.session_key

    disclaimer_seen = request.session.get('disclaimer_seen', False)

    if request.method == 'POST':
        # Mark the disclaimer as seen for this session
        request.session['disclaimer_seen'] = True
        return redirect("/")
        # return render(request, 'home.html', {'disclaimer_seen': disclaimer_seen})
    else:
        return render(request, 'home.html', {'disclaimer_seen': disclaimer_seen})
    # return render(request, 'home.html')

def inputideas_form(request,id=0):
    form=ideaForm() 

# def inputideas_form(request,id=0):
#     form=ideaForm()
#     selected_town = None
#     if request.method == 'POST':
#         form=ideaForm(request.POST)
#         if form.is_valid():
#             town = form.cleaned_data['town']
#             area = form.cleaned_data['area']
#             idea = form.cleaned_data['idea']
#             name = form.cleaned_data['name']
#             email = form.cleaned_data['email']
#             selected_town = town # pass this to the idea list form
            
#             if profanity.contains_profanity(idea):
#                 # Save the profane idea to the ProfaneIdeas table
#                 profane_idea = ProfaneIdeas(town=town, area=area, idea=idea, name=name, email=email)
#                 profane_idea.save()
#                 # return HttpResponse("Your idea contains profanity and has been flagged.")
#                 # return render(request,'idea_list.html')
#                 return redirect('idea_success')
#             else:
#                 # Save the new idea to the regular ideas table
#                 new_idea = form.save()
#             # Save the new idea to the database
#             # new_idea = form.save()
            

#             # Create a dictionary to store the summary text for each town and area combination
#             summary_text_by_town_area = {}

#             # Filter the ideas queryset based on the town and area fields
#             ideas_queryset = ideas.objects.filter(town=town, area=area)
        
#             # Pass the filtered queryset to the generate_summary method and store the summary text in the dictionary
#             if ideas_queryset.count() > 3:
#                 iSummary.objects.filter(town=town, area=area).update(isActive=False)
#                 summary_text = generate_summary(ideas_queryset, 3)
#                 summary_text_by_town_area[f"{town}-{area}"] = summary_text
#                 for i in summary_text.split("*"):
#                     print (i)
#                     summary = iSummary(Summary=i,isActive=True, town=town, area=area)
#                     summary.save()
#                     summary.ideas.add(new_idea)
#                 # Pass the dictionary to the template as the context variable
#                 sSections=load_summary_sections()
#                 context={'form': form,'sSections': sSections,'selected_town': selected_town}
#                 # return render(request,'idea_list.html',context)
#                 return redirect('idea_success')
#             else:
#                 iSummary_queryset = ideas.objects.filter(town=town, area=area)
#                 summary_text_by_town_area[f"{town}-{area}"] = iSummary_queryset
#                 summary = iSummary(Summary=idea,isActive=True, town=town, area=area)
#                 summary.save()
#                 summary.ideas.add(new_idea)
#                 # Pass the dictionary to the template as the context variable
#                 sSections=load_summary_sections()
#                 context={'form': form,'sSections': sSections,'selected_town': selected_town}
#                 # return redirect('list')
#                 return redirect('idea_success')
#                 # return render(request,'idea_list.html',context)
#     else:
#         form = ideaForm()
#         sSections=load_summary_sections()
#         context={'form': form,'sSections': sSections,'selected_town': selected_town}
#         return render(request, 'inputideas.html', {'form': form,'context': context})
# =================================
# This function mostly remains the same but now relies on the updated load_summary_sections
def inputideas_form(request, id=0):
    form = ideaForm()
    selected_town = None
    if request.method == 'POST':
        form = ideaForm(request.POST)
        if form.is_valid():
            town = form.cleaned_data['town']
            area = form.cleaned_data['area']
            idea = form.cleaned_data['idea']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            selected_town = town  # pass this to the idea list form

            if profanity.contains_profanity(idea):
                profane_idea = ProfaneIdeas(town=town, area=area, idea=idea, name=name, email=email)
                profane_idea.save()
                return redirect('idea_success')
            else:
                new_idea = form.save()

            summary_text_by_town_area = {}

            ideas_queryset = ideas.objects.filter(town=town, area=area)

            if ideas_queryset.count() > 3:
                iSummary.objects.filter(town=town, area=area).update(isActive=False)
                summary_text = generate_summary(ideas_queryset, 3)
                summary_text_by_town_area[f"{town}-{area}"] = summary_text
                for i in summary_text.split("*"):
                    summary = iSummary(Summary=i, isActive=True, town=town, area=area)
                    summary.save()
                    summary.ideas.add(new_idea)
                sSections = load_summary_sections()
                context = {'form': form, 'sSections': sSections, 'selected_town': selected_town}
                return redirect('idea_success')
            else:
                iSummary_queryset = ideas.objects.filter(town=town, area=area)
                summary_text_by_town_area[f"{town}-{area}"] = iSummary_queryset
                summary = iSummary(Summary=idea, isActive=True, town=town, area=area)
                summary.save()
                summary.ideas.add(new_idea)
                sSections = load_summary_sections()
                context = {'form': form, 'sSections': sSections, 'selected_town': selected_town}
                return redirect('idea_success')
    else:
        form = ideaForm()
        sSections = load_summary_sections()
        context = {'form': form, 'sSections': sSections, 'selected_town': selected_town}
        return render(request, 'inputideas.html', {'form': form, 'context': context})
# =================================


def idea_list(request):
    # idea_all=ideas.objects.all()

    sSections=load_summary_sections()   
    context={'sSections':sSections}
    return render(request,'idea_list.html',context)


def idea_update(request,id):

    emp=ideas.objects.get(pk=id)
    form=ideaForm(instance=emp)
    if request.method=='POST':
        form=ideaForm(request.POST,instance=emp)
        if form.is_valid():
            form.save()
        return redirect('list')
    context={'form': form}
    return render(request,'idea_update.html',context)

def about(request):
    return render(request, 'about.html')

from .forms import ideaForm, feedbackForm

def feedback(request):
    if request.method == 'POST':
        form = feedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the Feedback model
            # Add any additional logic or redirects after saving the feedback
            print("Feedback form Submitted")
            # Redirect the user to a success page or a different view
            return redirect('feedback_success')  # Create a URL pattern for 'feedback_success'
        else:
            print(form.errors)  # Print any form errors for debugging
    else:
        form = feedbackForm()
    
    context = {'form': form}
    return render(request, 'feedback.html', context)

def feedback_success(request):
    return render(request, 'feedback_success.html')


def idea_success(request):
    return render(request, 'idea_success.html')

def how_to(request):
    return render(request, 'howto.html')