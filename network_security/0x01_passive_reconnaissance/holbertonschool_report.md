# Holberton School Domain Analysis Report

## Overview
This document summarizes the information collected regarding the domain and subdomains of `holbertonschool.com`. The analysis includes IP ranges, technologies and frameworks, SSL certificate details, and server configurations.

---

## IP Ranges
The following IP addresses were identified for the `holbertonschool.com` domain and its subdomains:
- **35.180.27.154**  
  - Host: `ec2-35-180-27-154.eu-west-3.compute.amazonaws.com`
  - Service Provider: Amazon Data Services France  
  - Location: Paris, France  

- **52.47.143.83**  
  - Host: `ec2-52-47-143-83.eu-west-3.compute.amazonaws.com`
  - Subdomain: `yriry2.holbertonschool.com`
  - Service Provider: Amazon Data Services France  
  - Location: Paris, France  

---

## Subdomains and Services
### **`holbertonschool.com`**
- **Status:** HTTP/1.1 301 Moved Permanently  
- **Server:** nginx/1.18.0 (Ubuntu)  
- **Response Header:**
  - `Content-Type: text/html`
  - `Connection: keep-alive`
  - `Location: http://holbertonschool.com`

### **`yriry2.holbertonschool.com`**
- **Status:** HTTP/1.1 200 OK  
- **Server:** nginx  
- **Response Headers:**
  - `X-Frame-Options: SAMEORIGIN`
  - `X-XSS-Protection: 0`
  - `X-Content-Type-Options: nosniff`
  - `X-Download-Options: noopen`

---

## SSL Certificate Details
### SSL Certificate for `yriry2.holbertonschool.com`:
- **Issuer:** Let's Encrypt  
- **Supported SSL Versions:**  
  - TLSv1.2  
  - TLSv1.3  
- **Certificate Details:**
  - **Common Name (CN):** `yriry2.holbertonschool.com`
  - **Organization (O):** N/A  

---

## Technologies and Frameworks
### Web Servers
- **Nginx:** Versions identified include:
  - nginx/1.18.0 (Ubuntu)
  - nginx/1.21.6

### Security Features
- **SSL:** Enabled and configured using Let's Encrypt.  
- **HTTP Security Headers:**
  - `X-Frame-Options: SAMEORIGIN`
  - `X-XSS-Protection: 0`
  - `X-Content-Type-Options: nosniff`
  - `X-Download-Options: noopen`

---

## Notes
- The subdomain `yriry2.holbertonschool.com` appears to host a level 2 forum for the Holberton School.  
- HTTP redirections are configured for the main domain (`holbertonschool.com`) to avoid downtime or misrouting.  
- SSL/TLS configurations are up-to-date, with support for modern versions (TLSv1.2 and TLSv1.3).  

---

## Conclusion
The `holbertonschool.com` domain and its subdomains utilize robust server configurations with industry-standard security practices. Hosted on Amazon's infrastructure, it ensures scalability and reliability.
