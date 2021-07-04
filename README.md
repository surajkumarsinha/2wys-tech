<h2>The project Boiler plate</h2>

```bash
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
      <li>djangorestframework
      <li>django-cors-headers
      <li>mysqlclient
      <li>djangorestframework_simplejwt
      <li>djoser
      <li>django-recaptcha
      <li>django-axes
      <li>pyjwt
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

