<h2>The project Boiler plate</h2>
<h4>To be updated</h4>

```
bash


< PROJECT ROOT >
   |
   |
   |
   |-- Api/                           # Implements app logic and serve the static assets
       |-- wsgi.py                        # Start the app in production
       |-- urls.py                        # Define URLs served by all apps/nodes
           |-- url path                   ### localhost:8000/api/
    
       |-- settings.py                    # All the settings for the app
       
       |-- static/
       |    |-- <css, JS, images>         # CSS files, Javascripts files
                             
   
   |-- mainapp/

         |-- authentication/                     # Handles auth routes (login and register)
         |    |
         |    |-- urls.py                        # Define authentication routes  
         |        |-- url path                   ### localhost:8000/api/Acutes/{SignIn or SignUp}  
         |
         |    |-- models.py                      # Define custom user model  
         |    |-- views.py                       # Handles login and registration  
         |    |-- serializers.py                 # Defines fields and properties of models  
         |    |-- authentication.py              # Define custom authentication methods 
         |    |-- settings.py                    # adds custom settings for auth
         |
         |
         |
         |-- fileSystem/                          
         |    |
         |    |-- views.py                       
         |    |-- urls.py                       
         |    |-- models.py                      
         |    |-- serializers.py                 
         |
         |
         |
         |-- userProfile/                          
         |    |
         |    |-- views.py                       
         |    |-- urls.py
         |
         |
         |
         |-- Sign/                          
         |    |
         |    |-- views.py                       
         |    |-- urls.py                       
         |    |-- models.py                      
         |    |-- serializers.py                         
         |        
         |        
         |        
         |-- utils/                          
         |    |
         |    |-- auth.py                       
         |    |-- files.py
         |
         |
         |--models.py                              # all model imports from subdirs
         |--apps.py 
         |--admin.py 


   |--media/
   |
   |
   |
   |-- venv                                # Inject Configuration via Environment
   |-- manage.py                           # Start the app - Django default start script
   |
   |-- ************************************************************************
```
   <br>
   <br>
   <br>
   <br>

   <h3>Pip Requirements</h3>
   <ul>
      <li>asgiref==3.2.10
      <li>Django==3.1.1
      <li>django-appconf==1.0.4
      <li>django-cors-headers==3.5.0
      <li>django-ipware==3.0.1
      <li>django-restframework==0.0.1
      <li>django-templated-mail==1.1.1
      <li>djangorestframework==3.11.1
      <li>djangorestframework-simplejwt==4.4.0
      <li>djoser==2.0.5
      <li>PyJWT==1.7.1
      <li>pytz==2020.1
      <li>sqlparse==0.3.1
      <li>cryptography~=3.1
      <li>Pillow~=7.2.0
      <li>PyPDF2~=1.26.0
      <li>six~=1.15.0
      <li>requests~=2.24.0
   </ul>

```
   Base Notif. Class
  |                                    __________________________________________________
  |-- Email class      ------------->  |                                                 |          
  |                                    | Type : {'Reset Password', 'Invite Contributor'} |
  |-- Message class    ------------->  |                                                 |
  |                                    | Content : {'Dictionary'}                        | 
  |-- Push Notif class ------------->  |_________________________________________________|

```

