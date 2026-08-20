# Flask CI/CD Pipeline with GitHub Actions, Docker, Amazon ECR and EC2

## 1. Project Overview

This project demonstrates an end-to-end **CI/CD pipeline for a Flask application** using:

- GitHub
- GitHub Actions
- Python 3.12
- Pytest
- Docker
- Amazon ECR
- Amazon EC2
- AWS CLI

The pipeline automatically:

1. Checks out the source code.
2. Sets up Python.
3. Installs Python dependencies.
4. Runs Pytest.
5. Configures AWS credentials.
6. Logs in to Amazon ECR.
7. Builds the Docker image.
8. Pushes the image to Amazon ECR.
9. Connects to EC2 through SSH.
10. Pulls and runs the new Docker image.
11. Performs a Flask health check.
12. Reports deployment success or failure.

---

## 2. Architecture

```text
                         Developer
                             |
                             | git push
                             v
                  +-----------------------+
                  |       GitHub          |
                  | flask-cicd-assignment |
                  +-----------+-----------+
                              |
                              v
                  +-----------------------+
                  |    GitHub Actions     |
                  |-----------------------|
                  | Checkout              |
                  | Python 3.12           |
                  | Install dependencies  |
                  | Pytest                |
                  | AWS Authentication    |
                  | Docker Build          |
                  +-----------+-----------+
                              |
                              | docker push
                              v
                  +-----------------------+
                  |      Amazon ECR       |
                  | flask-cicd-assignment |
                  |                       |
                  | Docker Image          |
                  +-----------+-----------+
                              |
                              | docker pull
                              v
                  +-----------------------+
                  |       AWS EC2         |
                  |-----------------------|
                  | Docker                |
                  |   └── flask-app       |
                  |       Port 4000       |
                  +-----------+-----------+
                              |
                              | HTTP :4000
                              v
                       Flask Application
```

---

## 3. Repository Structure

```text
flask-cicd-assignment/
│
├── .github/
│   └── workflows/
│       └── cicd.yml
│
├── app.py
├── test_app.py
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore
```

---

## 4. Application Details

The Flask application runs on:

```text
Port: 4000
```

Health endpoint:

```text
http://localhost:4000/health
```

Expected health response:

```json
{
  "status": "healthy"
}
```

Application endpoint:

```text
http://localhost:4000/
```

Expected response:

```text
Hello from Flask CI/CD Pipeline!
```

> **Important:** The application and Dockerfile use port `4000`. Therefore the EC2 deployment uses `-p 4000:4000`.

---

# 5. Prerequisites

Install/configure the following:

- Git
- Python 3.12
- Docker
- AWS CLI
- AWS account
- GitHub account
- Amazon ECR repository
- Amazon EC2 instance

---

# 6. Clone the Repository

```bash
git clone https://github.com/praveen-coded/flask-cicd-assignment.git
cd flask-cicd-assignment
```

### Screenshot 1 — Clone Repository

Add your screenshot here:

<img width="1709" height="1028" alt="github-repo" src="https://github.com/user-attachments/assets/1379ef0e-60b2-43c1-8896-e92b6a102edf" />


---

# 7. Create Python Virtual Environment

On macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Verify Python:

```bash
python --version
```

Expected:

```text
Python 3.12.x
```


# 8. Install Dependencies

Install the project dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Verify pytest:

```bash
python -m pytest --version
```



# 9. Run Unit Tests Locally

Run:

```bash
python -m pytest -v
```

Expected result:

```text
============================= test session starts =============================
...
PASSED
...
============================== ... passed ==============================
```

### Screenshot 4 — Pytest Successful

<img width="1300" height="264" alt="pytest-successful" src="https://github.com/user-attachments/assets/657bde1c-33d4-4f70-8e4b-455a25834d00" />


# 10. Run Flask Application Locally

Start the application:

```bash
python app.py
```

The Flask application should start on:

```text
http://127.0.0.1:4000
```

Test the health endpoint from another terminal:

```bash
curl http://localhost:4000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

### Screenshot 5 — Flask Application Running

<img width="1924" height="1035" alt="App on local " src="https://github.com/user-attachments/assets/821ffc3f-31fa-48cd-8394-95d968c78136" />


---

# 11. Build Docker Image

Build the Docker image:

```bash
docker build -t flask-cicd-assignment .
```

Check the image:

```bash
docker images
```

### Screenshot 6 — Docker Image Built

<img width="1923" height="875" alt="ECR (image stored) " src="https://github.com/user-attachments/assets/fae994b6-ff5e-42db-9914-3d18eca2a24c" />


# 12. Run Docker Container Locally

Run:

```bash
docker run -d \
  --name flask-test \
  -p 4000:4000 \
  flask-cicd-assignment
```

Check:

```bash
docker ps
```

Test:

```bash
curl http://localhost:4000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

### Screenshot 7 — Docker Container Running

<img width="1478" height="878" alt="Image running on docker" src="https://github.com/user-attachments/assets/08104943-c5ff-4d2b-bcd6-e8fa85288b99" />

---

# 13. Create Amazon ECR Repository

Open AWS Console:

**Amazon ECR → Repositories → Create repository**

Create a private repository named:

```text
flask-cicd-assignment
```

Region:

```text
ap-south-1
```

The repository URI will look similar to:

```text
ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com/flask-cicd-assignment
```

### Screenshot 8 — ECR Repository

<img width="1923" height="875" alt="ECR (image stored) " src="https://github.com/user-attachments/assets/70a8edb3-acdc-4eb1-8da0-de0193611118" />

---

# 14. Create EC2 Instance

Create an Ubuntu EC2 instance.

Recommended assignment configuration:

```text
AMI: Ubuntu
Architecture: 64-bit
Instance type: t3.micro/t3.small or as required
Region: ap-south-1
```

Configure the Security Group.

Required inbound rules:

| Type | Port | Source |
|---|---:|---|
| SSH | 22 | Your IP |
| Custom TCP | 4000 | 0.0.0.0/0 |

> For a production environment, avoid exposing Flask directly and use a load balancer/reverse proxy.

### Screenshot 9 — EC2 Instance

```markdown
![Screenshot 9 - EC2 Instance](screenshots/09-ec2-instance.png)
```

![Screenshot 9 - EC2 Instance](screenshots/09-ec2-instance.png)

---

# 15. Configure EC2

SSH into the EC2 instance:

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Check Docker:

```bash
docker --version
```

Check AWS CLI:

```bash
aws --version
```

Check AWS identity:

```bash
aws sts get-caller-identity
```

Check curl:

```bash
curl --version
```

### Screenshot 10 — EC2 Environment

```markdown
![Screenshot 10 - EC2 Environment](screenshots/10-ec2-environment.png)
```

<img width="1911" height="867" alt="EC2 screenshot" src="https://github.com/user-attachments/assets/d6e77a74-756c-4bd8-ac5e-bdabbf1473b8" />


---

# 16. EC2 IAM Permissions

The EC2 instance needs permission to pull images from Amazon ECR.

Recommended approach:

**Attach an IAM role to the EC2 instance.**

The role should allow the EC2 instance to authenticate to ECR and pull images.

Avoid storing long-lived AWS access keys directly on the EC2 instance when an IAM role can be used.

### Screenshot 11 — EC2 IAM Role

```markdown
![Screenshot 11 - EC2 IAM Role](screenshots/11-ec2-iam-role.png)
```

<img width="1914" height="872" alt="IAM Role of ECR " src="https://github.com/user-attachments/assets/ed29a630-680a-4d80-91ec-e711fdd8d6fa" />


# 17. GitHub Actions Secrets

Open:

**GitHub → Repository → Settings → Secrets and variables → Actions**

Create these repository secrets:

| Secret | Example |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS access key |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key |
| `AWS_REGION` | `ap-south-1` |
| `ECR_REPOSITORY` | `flask-cicd-assignment` |
| `EC2_HOST` | EC2 public IP/DNS |
| `EC2_USER` | `ubuntu` |
| `EC2_SSH_KEY` | EC2 private SSH key |

> Never commit AWS access keys, secret keys, `.pem` files, or other credentials to GitHub.

### Screenshot 12 — GitHub Actions Secrets

```markdown
![Screenshot 12 - GitHub Actions Secrets](screenshots/12-github-secrets.png)
```

<img width="1694" height="1026" alt="GitHub Secrets" src="https://github.com/user-attachments/assets/a5cec678-ee9f-4d5c-8a57-a1298daea72a" />


---

# 18. GitHub Actions Workflow

The workflow is located at:

```text
.github/workflows/cicd.yml
```

The pipeline is triggered when code is pushed to:

```text
main
```

Workflow:

```text
push to main
      |
      v
Checkout
      |
      v
Setup Python
      |
      v
Install dependencies
      |
      v
Run pytest
      |
      v
Configure AWS
      |
      v
Login to ECR
      |
      v
Build Docker image
      |
      v
Push image to ECR
      |
      v
SSH to EC2
      |
      v
Pull image
      |
      v
Stop old container
      |
      v
Start new container
      |
      v
Health check
      |
      v
Deployment successful
```


# 19. Commit and Push Changes

Check Git status:

```bash
git status
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "Add Flask CI/CD pipeline"
```

Push:

```bash
git push origin main
```


---

# 20. GitHub Actions Execution

Open:

**GitHub → Repository → Actions**

Select:

**Flask CI/CD Pipeline**

The following steps should become successful:

```text
✓ Checkout source code
✓ Setup Python
✓ Install dependencies
✓ Run pytest
✓ Configure AWS credentials
✓ Login to Amazon ECR
✓ Set Docker image
✓ Build Docker image
✓ Push Docker image to ECR
✓ Deploy to EC2
✓ Success notification
```

### Screenshot 15 — GitHub Actions Successful

```markdown
![Screenshot 15 - GitHub Actions Success](screenshots/15-github-actions-success.png)
```

<img width="1914" height="895" alt="GitHub-Success-Pipeline" src="https://github.com/user-attachments/assets/1980deb4-2cf4-4eb3-80e0-48e19fdc0fbc" />


---

# 21. Verify Docker Image in ECR

Open:

**AWS Console → ECR → flask-cicd-assignment**

The pushed image should have a tag based on the GitHub commit SHA.

Example:

```text
IMAGE TAG:
a1b2c3d4e5f6...
```

### Screenshot 16 — Docker Image in ECR

```markdown
![Screenshot 16 - ECR Image](screenshots/16-ecr-image.png)
```

![Screenshot 16 - ECR Image](screenshots/16-ecr-image.png)

---

# 22. Verify Container on EC2

SSH into EC2:

```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_PUBLIC_IP
```

Check containers:

```bash
docker ps
```

Expected:

```text
CONTAINER ID   IMAGE                                      PORTS
xxxxxxxxxxxx   ...amazonaws.com/flask-cicd-assignment   0.0.0.0:4000->4000/tcp
```

Check logs:

```bash
docker logs flask-app
```


# 23. Verify Health Endpoint on EC2

Run on EC2:

```bash
curl --fail http://localhost:4000/health
```

Expected:

```json
{
  "status": "healthy"
}
```


# 24. Verify Application from Browser

Open:

```text
http://EC2_PUBLIC_IP:4000/
```

Expected:

```text
Hello from Flask CI/CD Pipeline!
```

Health endpoint:

```text
http://EC2_PUBLIC_IP:4000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

### Screenshot 19 — Flask Application in Browser

```markdown
![Screenshot 19 - Flask Application](screenshots/19-flask-browser.png)
```

<img width="1920" height="1034" alt="App on EC2" src="https://github.com/user-attachments/assets/3a96d9df-b104-4976-8f74-713a048e3944" />

---

# 25. Deployment Verification

The final deployment should look like:

```text
GitHub
   |
   | Push to main
   v
GitHub Actions
   |
   | pytest
   | docker build
   v
Amazon ECR
   |
   | docker pull
   v
Amazon EC2
   |
   v
Docker Container
   |
   v
Flask Application :4000
   |
   v
/health
   |
   v
{"status": "healthy"}
```



# 26. Troubleshooting

## Pytest command not found

If you see:

```text
zsh: command not found: pytest
```

Use:

```bash
python -m pytest -v
```

If pytest is not installed:

```bash
python -m pip install -r requirements.txt
```

---

## Docker container exits

Check:

```bash
docker ps -a
```

Then:

```bash
docker logs flask-app
```

---

## Health check fails

Check:

```bash
curl http://localhost:4000/health
```

Check container port:

```bash
docker ps
```

The mapping must be:

```text
0.0.0.0:4000->4000/tcp
```

---

## ECR login fails

Check AWS credentials:

```bash
aws sts get-caller-identity
```

Check region:

```bash
aws configure get region
```

Expected region:

```text
ap-south-1
```

---

## EC2 SSH deployment fails

Verify:

- EC2 public IP/DNS is correct.
- EC2 Security Group allows SSH port 22.
- `EC2_USER` is correct.
- `EC2_SSH_KEY` contains the complete private key.
- The EC2 instance is running.

---

## GitHub Actions fails at pytest

Open:

**GitHub → Actions → Flask CI/CD Pipeline → Failed Run → Run pytest**

Review the pytest output.

Run the same test locally:

```bash
python -m pytest -v
```

---

# 27. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Web framework |
| Pytest | Unit testing |
| Docker | Application containerization |
| GitHub | Source code repository |
| GitHub Actions | CI/CD automation |
| Amazon ECR | Docker image registry |
| Amazon EC2 | Application deployment |
| AWS CLI | AWS command-line operations |

---

# 28. Final Result

The completed project provides an automated CI/CD workflow:

```text
Developer pushes code
        ↓
GitHub
        ↓
GitHub Actions
        ↓
Run Pytest
        ↓
Build Docker Image
        ↓
Push Image to Amazon ECR
        ↓
SSH to EC2
        ↓
Pull Latest Image
        ↓
Stop Old Container
        ↓
Start New Container
        ↓
Health Check
        ↓
Application Successfully Deployed
```

The Flask application is available on:

```text
http://EC2_PUBLIC_IP:4000/
```

Health check:

```text
http://EC2_PUBLIC_IP:4000/health
```

---

## Repository

GitHub repository:

https://github.com/praveen-coded/flask-cicd-assignment

## Workflow

```text
.github/workflows/cicd.yml
```
