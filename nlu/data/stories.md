## thanks
* thank
    - utter_noworries
    - utter_anything_else

## bye
* bye
    - utter_bye

## greet
* greet OR enter_data{"name": "akela"}
    - action_greet_user
    
## sales form   
* contact_sales
    - sales_form                   <!--Run the sales_form action-->
    - form{"name": "sales_form"}   <!--Activate the form-->
    - form{"name": null}           <!--Deactivate the form-->
    
## adress
* adress
    - action_adress 