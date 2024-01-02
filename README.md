# Fleet Branding Management Platform

![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg) 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue.svg)](https://linkedin.com/in/garayevarif/)

fleet-branding-panel - is a fleet management web application platform. This platform was initially created for fleet owners. Branding and documentation monitoring is they key idea of this project. 
The project solves a communication issues with clients, offering a centralized solution where fleet owners and clients can create applications by uploading media content related to fleet-branded cars. Clients can also request the deletion of cars. This project acts like a communication bridge, improving internal company processes.

---

## **Contents**

- [Overview](#overview)
- [Features](#features)
- [Technical Specifications](#technical-specifications)
- [Services Design](#services-design)
- [Entity Design](#entity-design)
- [Autoscaling](#autoscaling)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## **Overview**

fleet-branding-panel - is a full-stack web application platform built using the monolithic MVC architectural pattern and Server-side rendering (SSR) with the Jinja templating engine. It offers various services and features, for various user authorizations.

---

## **Features**

### **Clients**

- Asynchronous media uploads (video/image).
- Request a car deletion with comments.

### **Admin Users**

- Modify application status (Approve, Reject, or Reset).
- Audit and set comment.
- Search for incoming applications.
- Create "fleet company" and user related.
- Set passwords for user.
- Export entity report (CSV).

---

## **Technical Specifications**

### **Programming Languages and Frameworks**

- **Architectural Pattern:** MVC.
- **Frontend:** HTML, CSS, Vanilla JavaScript, jQuery, and Tailwind CSS.
- **Backend:** Python, Flask, SQLAlchemy, PostgreSQL.
- **Authentication:** Session cookies, Server-side sessions.
- **Security:** CSRF tokens and XSS prevention.
- **Deployment:** Google Cloud Run (Serverless), Containerization (Docker), Gunicorn Application Server (WSGI).

### **Services Design**

- **Upload Service:** API endpoint HTTP requests sent binary data by chunks, to bypass GCP Cloud Run HTTP request limits (32MB). Trace previous chunked request to squash binary data on the server.
- **Search Service:** Implement short polling and JavaScript event handlers to browse incoming applications and cars.
- **User-registration Service:** Validate both "fleet company" and user account creation. Utilize Blowfish-based cryptographic function to securely store password in the database.

### **Entity Diagram**

#### **Applications**
Here's an overview of the entities in the database:
```plaintext
class applications {
        integer car_id_fkey
        integer users_id_fkey
        timestamp date_applied
        integer type_of_application
        text folder_uuid
        text quote
        integer is_archived
        text filename
        text b_comment
        integer is_requested_to_delete
        text application_status
        integer id
	}
	
	
class cars {
        bigint internal_car_id
        text internal_car_reg_number
        text internal_car_vin_no
        text internal_car_model
        integer internal_car_year
        text internal_source
        text internal_car_color
        text internal_car_status
        integer company_id_fkey
        date internal_car_date
        integer id
        }
        
        
class company {
        text internal_company_name
        bigint internal_company_id
        text internal_company_status
        bigint internal_company_balance_ref
        timestamp date_added
        integer id
	}


class roles {
        text description
        text role_name
        integer id
        }
        
        
class userRoles {
        integer user_fkey
        integer role_fkey
        integer id
	}		
	
	
class users {
        text username
        text password
        text email
        text mobile
        timestamp date_added
        integer is_admin
        text internal_company_manager_id
        text alternative_mobile
        integer company_id_fkey
        integer id
	}
```
**Entity Relationships:**

- `applications` → `cars` : `car_id_fkey:id`
- `applications` → `users` : `users_id_fkey:id`
- `cars` → `company` : `company_id_fkey:id`
- `userRoles` → `roles` : `role_fkey:id`
- `userRoles` → `users` : `user_fkey:id`
- `users` → `company` : `company_id_fkey:id`


---

## **Deployment**

The application is deployed on Google Cloud Run - a serverless Google product that offers scalability and reliability. Docker is used for containerization, while the Gunicorn Application Server handles WSGI and forking.

---

## **Autoscaling**

Autoscaling capabilities are enabled by default in the GCP Cloud Run configuration. Google Cloud Run handles load-balancing between WSGI workers on our behalf, maintaining optimal performance and resource utilization.

---


## **License**

This project is licensed under the [MIT License](LICENSE).
