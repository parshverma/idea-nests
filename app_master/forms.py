from django.forms import ModelForm
# from crispy forms
# https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html


from .models import ideas, Feedback


class ideaForm(ModelForm):
    class Meta:
        model=ideas
        fields='__all__'
        labels={
            'town': 'Town',
            'name': 'Name',
            'email': 'Email',
            'idea': 'Idea',
            'area': 'Area',   
        }
    def __init__(self, *args, **kwargs):
        super(ideaForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False     
        

from .models import ideas, Feedback

class feedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ('name', 'email', 'details', 'town') 
        
    def __init__(self, *args, **kwargs):
        super(feedbackForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = False 
        


    # class Meta:
    #     model = Feedback
    #     exclude = []
   
# def __init__(self,*args, **kwargs):
#     super(ideaForm, self).__init__(*args, **kwargs)
#     self.fields['town'].empty_label="Select your Town"
#     self.fields['town'].required=True