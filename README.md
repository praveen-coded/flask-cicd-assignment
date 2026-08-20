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

```
(github-repo.png)
```

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

```markdown
![Screenshot 4 - Pytest Successful](screenshots/04-pytest-success.png)
```

![Screenshot 4 - Pytest Successful](screenshots/04-pytest-success.png)

---

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

```markdown
![Screenshot 5 - Flask Application Running](screenshots/05-flask-running.png)
```

![Screenshot 5 - Flask Application Running](screenshots/05-flask-running.png)

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

```markdown
![Screenshot 6 - Docker Image](screenshots/06-docker-image.png)
```

![Screenshot 6 - Docker Image](screenshots/06-docker-image.png)

---

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

```markdown
![Screenshot 7 - Docker Container](screenshots/07-docker-container.png)
```

![Screenshot 7 - Docker Container](screenshots/07-docker-container.png)

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

```markdown
![Screenshot 8 - ECR Repository](screenshots/08-ecr-repository.png)
```

![Screenshot 8 - ECR Repository](screenshots/08-ecr-repository.png)

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

![Screenshot 10 - EC2 Environment](screenshots/10-ec2-environment.png)

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

![Screenshot 11 - EC2 IAM Role](screenshots/11-ec2-iam-role.png)

---

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

![Screenshot 12 - GitHub Actions Secrets](screenshots/12-github-secrets.png)

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

### Screenshot 13 — Workflow File

```markdown
![Screenshot 13 - CI/CD Workflow](screenshots/13-cicd-workflow.png)
```

![Screenshot 13 - CI/CD Workflow](screenshots/13-cicd-workflow.png)

---

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

### Screenshot 14 — Git Push

```markdown
![Screenshot 14 - Git Push](screenshots/14-git-push.png)
```

![Screenshot 14 - Git Push](screenshots/14-git-push.png)

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

![Screenshot 15 - GitHub Actions Success](screenshots/15-github-actions-success.png)

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

### Screenshot 17 — Flask Container on EC2

```markdown
![Screenshot 17 - EC2 Docker Container](screenshots/17-ec2-container.png)
```

![Screenshot 17 - EC2 Docker Container](screenshots/17-ec2-container.png)

---

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

### Screenshot 18 — Health Check

```markdown
![Screenshot 18 - Health Check](screenshots/18-health-check.png)
```

![Screenshot 18 - Health Check](screenshots/18-health-check.png)

---

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

![Screenshot 19 - Flask Application](screenshots/19-flask-browser.png)

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

### Screenshot 20 — Final Deployment

```markdown
![Screenshot 20 - Final Deployment](screenshots/20-final-deployment.png)
```

![Screenshot 20 - Final Deployment](screenshots/20-final-deployment.png)

---

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

# 27. Submission Screenshot Checklist

For assignment submission, capture the following screenshots:

- [ ] GitHub repository
- [ ] Project files
- [ ] Python environment
- [ ] Dependencies installed
- [ ] Pytest successful
- [ ] Flask application running locally
- [ ] Docker image built
- [ ] Docker container running
- [ ] ECR repository
- [ ] EC2 instance
- [ ] EC2 IAM role
- [ ] GitHub Actions Secrets page
- [ ] CI/CD workflow file
- [ ] Git push
- [ ] GitHub Actions successful
- [ ] Docker image available in ECR
- [ ] Flask container running on EC2
- [ ] Health endpoint successful
- [ ] Flask application accessible from browser
- [ ] Final deployment successful

> **Security:** Do not capture or submit screenshots that reveal AWS secret access keys, private SSH keys, passwords, or other sensitive credentials. If a secret value appears in a screenshot, remove/redact it before submission.

---

# 28. Technologies Used

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

# 29. Final Result

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
