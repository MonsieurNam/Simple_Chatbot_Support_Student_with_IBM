#A simple chatbot support school in student management and chat with everythings about school

##Chatbot and db2
- Access to waston assistant and db2 in IBM Cloud
- Create your chatbot one and upload your data to db2

##How to run
1. Create .env file that contain all db2 IBM-API and your secreckey 
    secret_key = 'your_secrec_key'
    dsn_hostname = 'your_db2_host_name'  
    dsn_uid = 'your_db2_uid' 
    dsn_pwd = 'your_db2_password'  
    dsn_port = 'your_db2_port'  
    dsn_database = "your_db2_dsn"  
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_protocol = "TCPIP"
    dsn_security = "SSL"
3. pip install -r requirement.txt
4. python web.py
5. Access to your local host: http://127.0.0.1:5000
