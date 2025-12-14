

# Crowdfunding Back End
Yasmine Azzaoui

## Planning:
### Concept/Name
Name: Dorfkin
Concept: Help marginalised communities stay connected by democratising child care, in a give and take village model.

### Intended Audience/User Stories
Target audience: Single Parents, Families that migrated and don’t have a safety net, people with disabilities or with children that need extra care, families that are going through hardship.

These individuals will create fundraisers to have other users/supporters help them with their childcare, in return they will also offer help and support to other parents in need

### Front End Pages/Functionality
- Homepage
    - Displays all fundraisers in ones city.
    - Logged in user can scroll through and filter by age of child and if child requires special support
    - User can create fundraiser on homepage to create buttom at the top right.
- Fundraiser details
    - Logged in user can see a detailed view of the fundraiser including any children attached to it and details about their personalisty 
    - Logged in user can decide to pledge money or if they have a bluecard even time. '
    - Annonymus user is able to pledge time, however, can't get more information on the children, nor can they pledge time
    - Logged in user without bluecard can see details of the children attached to the fundraiser, however, they can only pledge money. 

### API Spec
{{ Fill out the table below to define your endpoints. An example of what this might look like is shown at the bottom of the page. 

It might look messy here in the PDF, but once it's rendered it looks very neat! 

It can be helpful to keep the markdown preview open in VS Code so that you can see what you're typing more easily. }}

| URL | HTTP Method | Purpose | Request Body | Success Response Code | Authentication/Authorisation |
   URL	HTTP Method	Purpose	Request Body	Success Response Code	Authentication/Authorisation
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/users/	POST	Create a user with a blue card	"{
       ""username"": ""blueyholder"",
       ""email"": ""bluey@example.com"",
       ""password"": ""Password123!"",
       ""bluecard"": true,
        ""is_staff"": false,
        ""first_name"": ""blair"",
      ""last_name"": ""barc""
   }"	201	
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/users/	POST	Create a user without blue card	"{
       ""username"": ""noblueyholder"",
       ""email"": ""nobluey@example.com"",
       ""password"": ""Password123!"",
       ""bluecard"": false,
        ""is_staff"": false,
        ""first_name"": ""Noel"",
      ""last_name"": ""Arc""
   }"	201	
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/users/	POST	Create a user who will own the fundraiser used in example (parent)	"{
       ""username"": ""Parent1"",
       ""email"": ""parent@example.com"",
       ""password"": ""Password123!"",
       ""bluecard"": true,
        ""is_staff"": false,
        ""first_name"": ""Laila"",
      ""last_name"": ""Arc""
   }"	201	
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/api-token-auth/	POST	Token for Bluecard user	"
   {
       ""username"": ""blueyholder"",
       ""password"": ""Password123!""
   }"	200	4472501bbd0a94e90205231dfcfa86ca46e4d9cb
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/api-token-auth/	POST	Token for no Bluecard user	"
   {
       ""username"": ""noblueyholder"",
       ""password"": ""Password123!""
   }"	200	ca74bf5be4ee27ee6b69d0adbd580351e5643a68
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/api-token-auth/	POST	Token for Parent	"
   {
       ""username"": ""Parent1"",
       ""password"": ""Password123!""
   }"		f2642abb7669ea1067c793033cd27759c525d349
   https://dorfkind-production-app-4779995aedb8.herokuapp.com/fundraisers/	POST	I wanted to create a fundraiser, however, I tried all day and it didn't work with horoku so decided to do it in host	"{
     ""title"": ""Support Kiel's Therapy"",
     ""description"": ""Raising funds for developmental therapy support and time to look after him."",
     ""goal"": 5000,
     ""is_open"": true
   }"	500	
   http://localhost:8000/fundraisers/	POST	Parent Fundraiser	"{
     ""title"": ""Support Kiel's Therapy"",
     ""description"": ""Raising funds for developmental therapy support and time to look after him."",
     ""goal"": 5000,
     ""is_open"": true
   }"	201	


    SEE IMAGES IN FOLDER
    	

### DB Schema
![]( {{ ./relative/path/to/your/schema/image.png }} )