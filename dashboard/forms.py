from django import forms
from .models import CharacteristicModel, GlobalAspects, GlobalStrengths, QuestionModel, ReportModel, FactorModel ,UserModel, TaskModel

class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportModel
        fields = ['name', 'description', 'image', 'end_date', 'status']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter report name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a description...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class FactorForm(forms.ModelForm):
    class Meta:
        model = FactorModel
        fields = ['name', 'content', 'google_doc_url', 'status', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'google_doc_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://docs.google.com/document/...'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class CharacteristicForm(forms.ModelForm):
    class Meta:
        model = CharacteristicModel
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter characteristic title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write a description...'
            }),
        }

# ... New characteristic development form

class CharacteristicDevelopForm(forms.Form):
    strength_new = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new strength...'
        })
    )
    strength_existent = forms.ModelChoiceField(
        queryset=GlobalStrengths.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    aspect_new = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new aspect to improve...'
        })
    )
    aspect_existent = forms.ModelChoiceField(
        queryset=GlobalAspects.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['profile_picture']

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if not picture.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Por favor, cargue una imagen válida (JPG o PNG).")
        return picture
    
# New QuestionForm
class QuestionForm(forms.ModelForm):
    txt_file = forms.FileField(
        required=False,
        label="Cargar archivo TXT",
        widget=forms.FileInput(attrs={'accept': '.txt', 'class': 'form-control'})
    )

    class Meta:
        model = QuestionModel
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter question title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your question...'
            }),
        }

    def clean_txt_file(self):
        txt_file = self.cleaned_data.get('txt_file')
        if txt_file:
            if not txt_file.name.lower().endswith('.txt'):
                raise forms.ValidationError("Solo se permiten archivos .txt")
            try:
                content = txt_file.read().decode('utf-8')
                return content
            except Exception as e:
                raise forms.ValidationError(f"Error al leer el archivo: {str(e)}")
        return None

# New AnswerForm
class AnswerForm(forms.Form):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your answer here...'
        })
    )

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ['title', 'due_date', 'assignee']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title'
            }),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'assignee': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class ReportFilterForm(forms.Form):
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name...'
        })
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All')] + ReportModel.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    created_by = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by creator username...'
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'placeholder': 'Select end date...'
        })
    )