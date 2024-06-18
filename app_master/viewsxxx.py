from django.shortcuts import render,redirect
# from .models import ideas,iSummary
from .models import ideas, iSummary, Feedback

# from .forms import ideaForm, feedbackForm
from .forms import ideaForm
from django.db.models import Prefetch

# Start idea concatenate
import mysql.connector
from django.db import connection
# def concatenate_ideas():
#     allIdeas = ideas.objects.values_list('idea',flat=True)
#     return ''.join(allIdeas)
# # print(concatenate_ideas())
# # End Idea concatenate

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

def concatenate_ideas(town, area):
    if town not in valid_towns or area not in valid_area:
        raise ValueError("Invalid town or category input.")
    with connection.cursor() as cursor:
        cursor.execute("SELECT idea FROM ideas WHERE town = %s and area = %s", [town, area])
        all_ideas = cursor.fetchall()
    return ''.join([i[0] for i in all_ideas])


# Start Summary code
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx

from nltk.tokenize import word_tokenize

def read_article(file_name):
    file = open(file_name, 'r')
    filedata = file.readlines()
    article = filedata[0].split(".")
    sentences=[]
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    sentences.pop()
    return sentences


def sentence_similarity(sent1, sent2, stopwords = None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower for w in sent2]
    all_words = list(set(sent1+sent2))
    
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)]+=1
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)]+=1
    return 1-cosine_distance(vector1, vector2)

def gen_sim_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2:
                continue
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

def generate_summary(ideas, top_n = 3):
    stop_words = stopwords.words('english')
    summarize_text= []
    # sentences = read_article(file_name)
    # sentences=[s.strip() for s in file_name.split(".")]

    sentences=[s.idea.strip() for s in ideas]
    sentences = [s for s in sentences if len(s)>0 and s not in stop_words]
    sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i],s)for i,s in enumerate(sentences)), reverse=True)
    for i in range(top_n):
        summarize_text.append("".join(ranked_sentence[i][1]))
   
    return ". ".join(summarize_text)
    
# generate_summary('/Users/amitnverma/Desktop/TCM/app_master/testCases.txt', 3)

# End Summary code


def load_summary_sections():
   
    summary_sections = []
    for town, area in town_area_combinations:
        summary_queryset = iSummary.objects.filter(town=town, area=area, isActive=True)
        summary_sections.append(summary_queryset)
    # return render(request, 'summary_template.html', {'summary_sections': summary_sections})
    if summary_sections==[]:
        # Need to check when this section executes
        return summary_sections
    else:
        return summary_sections


def home(request):
    return render(request, 'home.html')

def inputideas_form(request,id=0):
    form=ideaForm() 

def inputideas_form(request,id=0):
    form=ideaForm()
    if request.method == 'POST':
        form=ideaForm(request.POST)
        if form.is_valid():
            town = form.cleaned_data['town']
            area = form.cleaned_data['area']
            idea = form.cleaned_data['idea']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Save the new idea to the database
            new_idea = form.save()
            

            # Create a dictionary to store the summary text for each town and area combination
            summary_text_by_town_area = {}

            # Filter the ideas queryset based on the town and area fields
            ideas_queryset = ideas.objects.filter(town=town, area=area)
        
            # Pass the filtered queryset to the generate_summary method and store the summary text in the dictionary
            if ideas_queryset.count() > 3:
                iSummary.objects.filter(town=town, area=area).update(isActive=False)
                summary_text = generate_summary(ideas_queryset, 3)
                summary_text_by_town_area[f"{town}-{area}"] = summary_text
                for i in summary_text.split("."):
                    print (i)
                    summary = iSummary(Summary=i,isActive=True, town=town, area=area)
                    summary.save()
                    summary.ideas.add(new_idea)
                # Pass the dictionary to the template as the context variable
                sSections=load_summary_sections()
                context={'form': form,'sSections': sSections}
                return render(request,'idea_list.html',context)
            else:
                iSummary_queryset = ideas.objects.filter(town=town, area=area)
                summary_text_by_town_area[f"{town}-{area}"] = iSummary_queryset
                summary = iSummary(Summary=idea,isActive=True, town=town, area=area)
                summary.save()
                summary.ideas.add(new_idea)
                # Pass the dictionary to the template as the context variable
                sSections=load_summary_sections()
                context={'form': form,'sSections': sSections}
                return redirect('list')
                return render(request,'idea_list.html',context)
    else:
        form = ideaForm()
        sSections=load_summary_sections()
        context={'form': form,'sSections': sSections}
        return render(request, 'inputideas.html', {'form': form,'context': context})


def idea_list(request):
    # idea_all=ideas.objects.all()

    sSections=load_summary_sections()   
    context={'sSections':sSections}
    return render(request,'idea_list.html',context)




# def idea_list(request):
#     idea_all=ideas.objects.all()
#     context={'idea_all':idea_all}
#     return render(request,'idea_list.html',context)

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

# def feedback(request):
#     # print("Inside Feedback function")
#     return render(request, 'feedback.html')


# def feedback_form(request):
#     if request.method == 'POST':
#         form = feedbackForm(request.POST)
#         if form.is_valid():
#             form.save()
#             print("Feedback form Submitted")
#             return render(request, 'feedback.html')
#     else:
#         form = feedbackForm()
#     return render(request, 'feedback.html', {'form': form})

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