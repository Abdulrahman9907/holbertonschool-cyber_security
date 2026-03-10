# Holberton School - Passive Reconnaissance Report

## Target Domain
`holbertonschool.com`

---

## IP Ranges

| Subdomain | IP Address(es) | Provider |
|-----------|---------------|----------|
| holbertonschool.com | 198.202.211.1 | Webflow (CDN) |
| www.holbertonschool.com | 198.202.211.1 | Webflow (CDN) |
| apply.holbertonschool.com | 15.224.128.47, 52.47.213.199, 15.224.42.158 | AWS Elastic Beanstalk (eu-west-3) |
| blog.holbertonschool.com | 192.0.78.230, 192.0.78.131 | WordPress.com |
| assets.holbertonschool.com | 52.85.110.79, 52.85.110.47, 52.85.110.30, 52.85.110.57 | AWS CloudFront |
| fr.holbertonschool.com | 15.161.34.42, 35.152.117.67, 15.160.106.203 | Webflow / AWS |

### IP Ranges Summary
- `198.202.211.0/24` - Webflow CDN (main website)
- `15.224.0.0/14` - AWS EC2 (eu-west-3, Paris)
- `52.47.0.0/16` - AWS EC2 (eu-west-3)
- `52.85.0.0/16` - AWS CloudFront
- `192.0.78.0/24` - Automattic (WordPress.com)

---

## Technologies & Frameworks

### Main Website (holbertonschool.com / www)
- **Webflow** - Website builder / CMS
- **CDN**: Webflow CDN (proxy-ssl.webflow.com)
- **SSL/TLS**: HTTPS enabled

### Apply Portal (apply.holbertonschool.com)
- **AWS Elastic Beanstalk** - Application hosting
- **Region**: eu-west-3 (Paris)
- **Runtime**: Node.js / Ruby on Rails (intranet stack)

### Blog (blog.holbertonschool.com)
- **WordPress.com** - Blog platform (Automattic infrastructure)
- **PHP** - Backend language

### Assets (assets.holbertonschool.com)
- **AWS CloudFront** - CDN for static assets
- **Amazon S3** - Static file storage (likely origin)

### DNS Infrastructure
- **AWS Route 53** - DNS provider
  - `ns-1991.awsdns-56.co.uk`
  - `ns-343.awsdns-42.com`
  - `ns-957.awsdns-55.net`
  - `ns-1244.awsdns-27.org`

### Email Infrastructure
- **Google Workspace (Gmail)** - Email provider
  - `aspmx.l.google.com` (priority 1)
  - `alt1.aspmx.l.google.com` (priority 5)
  - `alt2.aspmx.l.google.com` (priority 5)
  - `alt3.aspmx.l.google.com` (priority 10)
  - `alt4.aspmx.l.google.com` (priority 10)

---

## Summary

Holberton School's infrastructure is entirely cloud-based, primarily using **AWS** services for hosting and content delivery, **Webflow** for their main marketing site, **WordPress.com** for the blog, and **Google Workspace** for email. DNS is managed through **AWS Route 53**. No on-premise infrastructure was identified through passive reconnaissance.