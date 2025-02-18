I'll help you understand Django forms comprehensively. Django forms are a powerful way to handle user input while providing validation, security, and clean data processing. Let's break this down step by step.

Forms in Django serve three main purposes: rendering HTML form elements, validating user input, and converting form data into Python objects. Understanding these aspects will help you build robust web applications.

Let's start with a basic example and build up to more complex scenarios:

```python
# forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

To use this form in a view and template:

```python
# views.py
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Access cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            # Process the data...
            return HttpResponse('Thank you for your message!')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
```

```html
<!-- templates/contact.html -->
<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Send</button>
</form>
```

Now, let's explore the key concepts in detail:

Form Fields: Django provides many field types to handle different kinds of data. Each field type handles validation and data conversion automatically:

```python
class AdvancedForm(forms.Form):
    # Text inputs
    title = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    
    # Numbers
    age = forms.IntegerField(min_value=0)
    rating = forms.FloatField(min_value=0, max_value=5)
    
    # Choices
    CHOICES = [('draft', 'Draft'), ('published', 'Published')]
    status = forms.ChoiceField(choices=CHOICES)
    
    # Date and time
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    # Files
    document = forms.FileField(required=False)
    
    # Boolean
    subscribe = forms.BooleanField(required=False)
```

Widgets are Django's representation of HTML input elements. They determine how fields are rendered in HTML:

```python
class StyleForm(forms.Form):
    # Custom widget attributes
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    
    # Custom select widget
    category = forms.ChoiceField(
        choices=[('tech', 'Technology'), ('art', 'Art')],
        widget=forms.Select(attrs={'class': 'custom-select'})
    )
```

Form validation is a crucial aspect. Django provides both built-in and custom validation:

```python
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    def clean_username(self):
        # Field-specific validation
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username
    
    def clean(self):
        # Cross-field validation
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Passwords don't match")
        
        return cleaned_data
```

ModelForms are a special type of form that work directly with Django models:

```python
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']
        # or use fields = '__all__' for all model fields
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'title': 'Article Title',
        }
        help_texts = {
            'category': 'Choose the most relevant category',
        }
```

For handling file uploads, you need to set the correct form encoding type:

```html
<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

And in your view:

```python
def upload_view(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Handle file upload
            uploaded_file = request.FILES['document']
            # Process the file...
    else:
        form = UploadForm()
    return render(request, 'upload.html', {'form': form})
```

Form rendering can be customized in several ways:

```html
<!-- Default rendering -->
{{ form.as_p }}  <!-- Wraps in <p> tags -->
{{ form.as_table }}  <!-- Renders as table rows -->
{{ form.as_ul }}  <!-- Renders as list items -->

<!-- Manual field rendering -->
<form method="POST">
    {% csrf_token %}
    <div class="form-group">
        {{ form.username.label_tag }}
        {{ form.username }}
        {{ form.username.errors }}
        {% if form.username.help_text %}
            <small class="help-text">{{ form.username.help_text }}</small>
        {% endif %}
    </div>
    <!-- Repeat for other fields -->
</form>
```

Some advanced techniques include form inheritance and dynamic forms:

```python
class BaseProductForm(forms.Form):
    name = forms.CharField(max_length=100)
    price = forms.DecimalField(max_digits=10, decimal_places=2)

class DigitalProductForm(BaseProductForm):
    download_url = forms.URLField()

class PhysicalProductForm(BaseProductForm):
    weight = forms.FloatField()
    
# Dynamic form fields
class DynamicForm(forms.Form):
    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra_fields', [])
        super().__init__(*args, **kwargs)
        
        for field in extra_fields:
            self.fields[field['name']] = forms.CharField(
                label=field['label'],
                max_length=100
            )
```

Remember to handle form errors appropriately in your templates:

```html
{% if form.errors %}
    <div class="alert alert-danger">
        <ul>
            {% for field in form %}
                {% for error in field.errors %}
                    <li>{{ field.label }}: {{ error }}</li>
                {% endfor %}
            {% endfor %}
            {% for error in form.non_field_errors %}
                <li>{{ error }}</li>
            {% endfor %}
        </ul>
    </div>
{% endif %}
```
---
I'll provide an exhaustive explanation of Django forms, breaking down every aspect from fundamentals to advanced concepts. Let's build this knowledge systematically.

# 1. Understanding Django Forms: The Foundation

Django forms serve as a bridge between user input and your application's data processing. They handle three critical aspects:

1. Generating HTML form elements
2. Validating and processing user input
3. Converting form data into Python objects

Let's start with the basic structure and gradually explore more complex scenarios.

# 2. Form Types and Basic Structure

Django provides two main types of forms: Form and ModelForm. Let's examine both:

```python
# Regular Form
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

# ModelForm
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'author']
```

The key difference is that ModelForm automatically creates form fields based on your model fields, while regular Form gives you complete control over field definitions.

# 3. Field Types and Their Properties

Django provides an extensive collection of field types. Let's explore them with their properties:

```python
class ComprehensiveForm(forms.Form):
    # Text Fields
    name = forms.CharField(
        max_length=100,
        min_length=2,
        required=True,
        help_text="Enter your full name",
        initial="John Doe",
        strip=True  # Removes leading/trailing whitespace
    )
    
    # Numeric Fields
    age = forms.IntegerField(
        min_value=0,
        max_value=150,
        required=False
    )
    
    salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0
    )
    
    # Date and Time Fields
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%m/%d/%Y']
    )
    
    appointment_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    # Choice Fields
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect
    )
    
    # Multiple Choice Fields
    HOBBIES = [
        ('reading', 'Reading'),
        ('sports', 'Sports'),
        ('music', 'Music')
    ]
    hobbies = forms.MultipleChoiceField(
        choices=HOBBIES,
        widget=forms.CheckboxSelectMultiple
    )
    
    # File Fields
    profile_picture = forms.ImageField(
        required=False,
        help_text="Upload a profile picture (max 5MB)",
        validators=[MaxFileSizeValidator(5 * 1024 * 1024)]  # Custom validator
    )
    
    # Boolean Fields
    subscribe = forms.BooleanField(
        required=False,
        initial=True,
        label="Subscribe to newsletter"
    )
```

# 4. Advanced Form Processing in Views

Let's examine a comprehensive view that handles form processing:

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic.edit import FormView

# Function-based view approach
def contact_view(request):
    initial_data = {
        'name': request.user.get_full_name() if request.user.is_authenticated else '',
        'email': request.user.email if request.user.is_authenticated else ''
    }
    
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, initial=initial_data)
        if form.is_valid():
            try:
                # Access cleaned data
                cleaned_data = form.cleaned_data
                
                # Process the form data
                name = cleaned_data['name']
                email = cleaned_data['email']
                message = cleaned_data['message']
                
                # Save or process data
                Contact.objects.create(**cleaned_data)
                
                # Add success message
                messages.success(request, 'Your message has been sent successfully!')
                
                # Redirect to success page
                return redirect('contact_success')
                
            except Exception as e:
                # Handle any errors during processing
                messages.error(request, f'An error occurred: {str(e)}')
                
    else:
        form = ContactForm(initial=initial_data)
    
    return render(request, 'contact.html', {
        'form': form,
        'title': 'Contact Us'
    })

# Class-based view approach
class ContactFormView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/success/'
    
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial.update({
                'name': self.request.user.get_full_name(),
                'email': self.request.user.email
            })
        return initial
    
    def form_valid(self, form):
        # Process the valid form data
        Contact.objects.create(**form.cleaned_data)
        messages.success(self.request, 'Message sent successfully!')
        return super().form_valid(form)
```

# 5. Form Validation and Custom Validators

Form validation is crucial for ensuring data integrity. Let's explore different validation approaches:

```python
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError

class RegistrationForm(forms.Form):
    # Field with multiple validators
    username = forms.CharField(
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex='^[a-zA-Z0-9]*$',
                message='Username must be alphanumeric'
            )
        ]
    )
    
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    # Custom field-level validation
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken.')
        return username
    
    # Custom form-level validation
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise ValidationError('Passwords do not match.')
            
            # Complex password validation
            if len(password) < 8:
                raise ValidationError('Password must be at least 8 characters.')
            if not any(char.isdigit() for char in password):
                raise ValidationError('Password must contain at least one number.')
            if not any(char.isupper() for char in password):
                raise ValidationError('Password must contain at least one uppercase letter.')
        
        return cleaned_data
```

# 6. Advanced Form Rendering and Templates

Let's look at comprehensive template rendering:

```html
{% extends 'base.html' %}

{% block content %}
<div class="form-container">
    {% if form.non_field_errors %}
        <div class="alert alert-danger">
            {% for error in form.non_field_errors %}
                <p>{{ error }}</p>
            {% endfor %}
        </div>
    {% endif %}

    <form method="POST" enctype="multipart/form-data" novalidate>
        {% csrf_token %}
        
        {% for field in form %}
            <div class="form-group {% if field.errors %}has-error{% endif %}">
                <label for="{{ field.id_for_label }}" class="form-label">
                    {{ field.label }}
                    {% if field.field.required %}
                        <span class="required">*</span>
                    {% endif %}
                </label>
                
                {{ field }}
                
                {% if field.help_text %}
                    <small class="form-text text-muted">{{ field.help_text }}</small>
                {% endif %}
                
                {% if field.errors %}
                    <div class="error-messages">
                        {% for error in field.errors %}
                            <span class="text-danger">{{ error }}</span>
                        {% endfor %}
                    </div>
                {% endif %}
            </div>
        {% endfor %}
        
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</div>
{% endblock %}
```

# 7. Dynamic Forms and Form Factory Patterns

Here's how to create dynamic forms based on runtime conditions:

```python
class DynamicModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)
        super().__init__(*args, **kwargs)
        
        # Dynamically modify fields based on user role
        if user_role == 'basic':
            # Remove advanced fields
            self.fields.pop('advanced_setting', None)
            
        # Add dynamic validation
        if user_role == 'admin':
            self.fields['title'].validators.append(
                MinLengthValidator(10)
            )
            
        # Modify field attributes
        for field_name, field in self.fields.items():
            # Add CSS classes
            field.widget.attrs['class'] = 'form-control'
            
            # Add placeholder text
            field.widget.attrs['placeholder'] = f'Enter {field_name}'

# Form Factory Pattern
def create_custom_form(fields_config):
    class CustomForm(forms.Form):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            
            for field_config in fields_config:
                field_type = field_config.get('type', forms.CharField)
                field_kwargs = field_config.get('kwargs', {})
                self.fields[field_config['name']] = field_type(**field_kwargs)
    
    return CustomForm

# Usage
fields_config = [
    {
        'name': 'title',
        'type': forms.CharField,
        'kwargs': {'max_length': 100}
    },
    {
        'name': 'age',
        'type': forms.IntegerField,
        'kwargs': {'min_value': 0}
    }
]

CustomForm = create_custom_form(fields_config)
```
---

Let me break this down into interconnected concepts to help build a clear understanding of Django's form validation and rendering system.

Let's start with validation methods - clean() and clean_fieldname():

The validation system in Django works like a series of quality control checkpoints. When a form is submitted, Django runs validation in a specific order:

1. The clean_fieldname() methods run first, handling individual field validation. Think of these as specialized inspectors who each check one specific aspect of the data. For example, clean_username() might check if a username is unique:

```python
def clean_username(self):
    username = self.cleaned_data['username']
    if User.objects.filter(username=username).exists():
        raise ValidationError('Username already taken')
    return username
```

Notice how clean_fieldname() methods must always return the value, even if unchanged. This is because the returned value becomes part of the cleaned_data dictionary that your form will use later.

2. The clean() method runs last, handling validation that involves multiple fields. Think of this as a supervisor who can look at how different pieces of data relate to each other. A classic example is password confirmation:

```python
def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    confirm = cleaned_data.get('confirm_password')
    
    if password and confirm and password != confirm:
        raise ValidationError("Passwords don't match")
    return cleaned_data
```

The clean() method receives all previously cleaned data, allowing it to perform cross-field validation. It's important to call super().clean() first to ensure you're working with data that's already passed basic validation.

Now, let's understand validators. These are reusable validation functions that you can attach to fields. Think of validators as pre-made inspection tools that you can apply wherever needed:

```python
from django.core.validators import MinLengthValidator, RegexValidator

username = forms.CharField(
    validators=[
        MinLengthValidator(3),
        RegexValidator(r'^[a-zA-Z0-9]+$', 'Only alphanumeric characters allowed')
    ]
)
```

Validators run before clean methods and are great for validation rules you might want to reuse across different forms or fields.

Moving on to ModelForm - this is Django's way of automatically creating a form based on a model. The key to understanding ModelForm is its Meta class, which acts like a configuration panel:

```python
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']
        exclude = ['author']  # Fields to exclude
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }
        labels = {
            'title': 'Article Title'
        }
        help_texts = {
            'category': 'Choose the most relevant category'
        }
        error_messages = {
            'title': {
                'required': 'Please provide a title'
            }
        }
```

The Meta class attributes control different aspects of how the form is created:
- fields/exclude: Control which model fields become form fields
- widgets: Customize how fields are rendered
- labels/help_texts: Customize field labels and help text
- error_messages: Customize validation error messages

Finally, let's clarify the distinction between fields and widgets. This is similar to the difference between data and its presentation:

Fields define:
- What type of data is acceptable
- How to validate the data
- How to convert between Python and form data

Widgets define:
- How the field appears in HTML
- How users interact with it
- What HTML attributes it should have

For example, a DateField (which handles date data) could use different widgets:
```python
# Same field type, different widgets
birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
birth_date = forms.DateField(widget=forms.SelectDateWidget())
```

The field ensures you get a valid date object, while the widget determines whether users see a calendar picker or dropdown menus.

The save() method in ModelForm deserves special mention. It handles converting form data into model instances:

```python
def save(self, commit=True):
    instance = super().save(commit=False)
    instance.author = self.user  # Add custom data
    if commit:
        instance.save()
    return instance
```

The commit parameter lets you control whether the data is immediately saved to the database, useful when you need to add data not collected by the form.

---

# CHATGPT

Here's a comprehensive tutorial on **Django Forms**, covering everything from basic usage to advanced techniques.

# Comprehensive Django Forms Tutorial

Django Forms provide an easy and secure way to handle user input and validation. This tutorial covers everything from the basics to advanced features.

---

## **1. Introduction to Django Forms**
Django provides a built-in `forms` module that simplifies form handling. A Django form is a Python class that maps fields to HTML form elements and performs validation.

### **Why Use Django Forms?**
- **Automatic validation**
- **Built-in security** (prevents SQL injection, XSS, and CSRF attacks)
- **Easier integration with Django models**
- **Customizable layout and styling**

---

## **2. Creating a Basic Django Form**
Define a form using Django’s `forms.Form` class:

```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
```

### **Rendering the Form in a Template**
Pass the form to the template in a Django view:

```python
from django.shortcuts import render
from .forms import ContactForm

def contact_view(request):
    form = ContactForm()
    return render(request, 'contact.html', {'form': form})
```

**`contact.html`**
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}  <!-- Renders the form with <p> tags -->
    <button type="submit">Submit</button>
</form>
```

---

## **3. Handling Form Submission**
Modify the view to handle form submission:

```python
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(name, email, message)  # Example: Log to console
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
```

### **Form Validation**
- `form.is_valid()` checks validation.
- `form.cleaned_data` gives sanitized input.

---

## **4. Model Forms (Forms Linked to Models)**
If your form fields match a Django model, use `forms.ModelForm`:

```python
from django import forms
from .models import Contact

class ContactModelForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
```

### **Using Model Forms in Views**
```python
def contact_view(request):
    if request.method == 'POST':
        form = ContactModelForm(request.POST)
        if form.is_valid():
            form.save()  # Saves data to the database
    else:
        form = ContactModelForm()
    
    return render(request, 'contact.html', {'form': form})
```

**Advantages of Model Forms**
- No need to manually define fields.
- Automatically saves data to the database.

---

## **5. Form Widgets & Customization**
Widgets control how form fields render in HTML.

```python
class CustomForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}))
```

### **Commonly Used Widgets**
- `forms.TextInput`
- `forms.Textarea`
- `forms.Select`
- `forms.CheckboxInput`
- `forms.FileInput`

---

## **6. Custom Validation**
Use `clean_<fieldname>()` for field-specific validation.

```python
class ContactForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@example.com'):
            raise forms.ValidationError("Only example.com emails are allowed.")
        return email
```

Use `clean()` for form-wide validation:

```python
def clean(self):
    cleaned_data = super().clean()
    email = cleaned_data.get('email')
    name = cleaned_data.get('name')

    if name and email and 'test' in name:
        self.add_error('name', "Name cannot contain 'test'")
```

---

## **7. File Upload in Django Forms**
Modify the form:

```python
class FileUploadForm(forms.Form):
    file = forms.FileField()
```

Modify the view:

```python
def upload_view(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            with open(f'uploads/{file.name}', 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
    else:
        form = FileUploadForm()

    return render(request, 'upload.html', {'form': form})
```

In the template:

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

---

## **8. Django Formsets (Multiple Forms)**
A formset allows multiple instances of a form.

```python
from django.forms import formset_factory

ContactFormSet = formset_factory(ContactForm, extra=2)

def contact_formset_view(request):
    formset = ContactFormSet()
    return render(request, 'formset.html', {'formset': formset})
```

In the template:

```html
<form method="post">
    {% csrf_token %}
    {{ formset.as_p }}
    <button type="submit">Submit</button>
</form>
```

---

## **9. Advanced Features**
### **1. Custom Form Rendering with `as_table` and `as_ul`**
```html
{{ form.as_table }}  <!-- Renders form as <tr><td> -->
{{ form.as_ul }}     <!-- Renders form as <li> -->
```

### **2. Using Bootstrap with Django Forms**
Modify your form:

```python
class BootstrapForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
```

Modify the template:

```html
<form method="post">
    {% csrf_token %}
    <div class="form-group">
        <label for="{{ form.name.id_for_label }}">Name</label>
        {{ form.name }}
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### **3. Custom Form Classes**
```python
class CustomContactForm(forms.Form):
    name = forms.CharField()
    
    class Meta:
        css_class = 'custom-css'
```
---

# Comprehensive Django-Bootstrap5 Tags Tutorial

The `django-bootstrap5` package provides a seamless integration of Bootstrap 5 components into Django templates using template tags. This tutorial covers all aspects of using `django-bootstrap5` tags, from installation to advanced customization.

---

## **1. Installation**
To get started, install the package via pip:

```bash
pip install django-bootstrap5
```

Then, add `'django_bootstrap5'` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'django_bootstrap5',
]
```

Load the `bootstrap5` template tag library in your templates:

```django
{% load bootstrap5 %}
```

---

## **2. Bootstrap 5 CSS & JavaScript Integration**
To include Bootstrap 5’s CSS and JavaScript in your templates, use:

```django
{% bootstrap_css %}
{% bootstrap_javascript %}
```

This will automatically insert the necessary Bootstrap assets in your HTML.

---

## **3. Bootstrap Forms**

### **3.1. Rendering Forms with Bootstrap**
You can render a form with Bootstrap styling using:

```django
{% bootstrap_form form %}
```

Example:

```django
<form method="post">
    {% csrf_token %}
    {% bootstrap_form my_form %}
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

### **3.2. Individual Form Fields**
You can render individual form fields with:

```django
{% bootstrap_field form.field_name %}
```

Example:

```django
{% bootstrap_field my_form.username %}
```

### **3.3. Form Buttons**
Bootstrap provides button rendering helpers:

```django
{% bootstrap_button "Submit" button_type="submit" button_class="btn-primary" %}
```

Equivalent HTML:

```html
<button type="submit" class="btn btn-primary">Submit</button>
```

### **3.4. Form Errors & Alerts**
You can display non-field form errors using:

```django
{% bootstrap_form_errors form type="all" %}
```

---

## **4. Bootstrap Components with Template Tags**

### **4.1. Bootstrap Alerts**
To display Bootstrap-styled alerts, use:

```django
{% bootstrap_messages %}
```

This will automatically render Django messages using Bootstrap alert styles.

Example:

```python
from django.contrib import messages

messages.success(request, "Your profile has been updated!")
```

Resulting HTML:

```html
<div class="alert alert-success" role="alert">
    Your profile has been updated!
</div>
```

### **4.2. Bootstrap Icons**
You can use Bootstrap icons with:

```django
{% bootstrap_icon "check-circle-fill" %}
```

Equivalent HTML:

```html
<svg class="bi bi-check-circle-fill" ...>...</svg>
```

### **4.3. Bootstrap Grid System**
Use Bootstrap’s grid system within Django templates:

```django
<div class="container">
    <div class="row">
        <div class="col-md-6">
            {% bootstrap_field my_form.email %}
        </div>
        <div class="col-md-6">
            {% bootstrap_field my_form.password %}
        </div>
    </div>
</div>
```

---

## **5. Customizing Bootstrap Integration**
You can configure `django-bootstrap5` by modifying settings in `settings.py`:

```python
BOOTSTRAP5 = {
    "css_url": {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "integrity": "...",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
    },
    "theme_url": None,  # Optional: Custom Bootstrap theme
}
```

---

## **6. Bootstrap Modals**
To use Bootstrap 5 modals in Django templates:

```django
<!-- Modal Trigger -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
    Open Modal
</button>

<!-- Modal -->
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Modal Title</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                {% bootstrap_form my_form %}
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="submit" class="btn btn-primary">Save changes</button>
            </div>
        </div>
    </div>
</div>
```

---

## **7. Bootstrap Navbar in Django**
```django
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">My Site</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" href="{% url 'home' %}">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="{% url 'about' %}">About</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

---

## **8. Bootstrap Toast Notifications**
Enable toast messages with:

```django
<div class="toast show" role="alert">
    <div class="toast-header">
        <strong class="me-auto">Notification</strong>
        <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    </div>
    <div class="toast-body">
        {% for message in messages %}
            {{ message }}
        {% endfor %}
    </div>
</div>
```

---

## **9. Handling Bootstrap Theming**
To apply a custom Bootstrap theme, set a theme URL in `settings.py`:

```python
BOOTSTRAP5 = {
    "theme_url": "https://bootswatch.com/5/flatly/bootstrap.min.css",
}
```

This will replace the default Bootstrap styles with the chosen theme.

---

## **10. Bootstrap Pagination**
You can use Bootstrap-styled pagination by modifying your template:

```django
<nav aria-label="Page navigation">
    <ul class="pagination">
        {% if page_obj.has_previous %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a>
            </li>
        {% endif %}
        <li class="page-item active">
            <a class="page-link" href="?page={{ page_obj.number }}">{{ page_obj.number }}</a>
        </li>
        {% if page_obj.has_next %}
            <li class="page-item">
                <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a>
            </li>
        {% endif %}
    </ul>
</nav>
```

---

