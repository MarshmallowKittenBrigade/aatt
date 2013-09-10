aatt
====

Automate All The Things
This is a very, very early version of this software.  Use at your own risk.

Installation
------------
To install the aatt web service, simply place the contents of the web directory into the root of your web server (or a virtualhost).  Run the sql from the db dir to create the database then create a database user.  Update includes/aatt_config.php to use your database credentials and voila!  Then you can either grab one of the client libraries or access the API directly.

Sample JSON
-----------
Here are some samples of what the JSON will look like.

#####CHECK:
>{"AUTH":{"APP":"app","ACCOUNT":"account","KEY":"key"},"ACT":"act","DATA":{"DEVICE":"device_id","CHECKS":{"endpoint_id_1":"attribute_id_1","end_point_id_2":"attribute_id_2"}}}

#####RECORD:
>{"AUTH":{"APP":"app","ACCOUNT":"account","KEY":"key"},"ACT":"act","DATA":{"DEVICE":"device_id","RECORDS":{"endpoint_id_1":"value","end_point_id_2":"value"}}}

#####CHECK RESPONSE:
>{"STATUS":"status","RESPONSE":{"endpoint_id_1":{"attribute_id":"state","attribute_id":"state"},"endpoint_id_2":{"attribute_id":"state","attribute_id":"state"}}}

#####RECORD RESPONSE:
>{"STATUS":"status","RESPONSE":{"RECORDED":"rows_recorded"}}
