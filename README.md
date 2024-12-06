# InternMatch

## Project Overview
InternMatch is a data-driven platform designed to transform the way companies find and recruit interns. By utilizing sophisticated algorithms to analyze and match resumes with job listings, the platform significantly reduces the time and effort involved in screening candidates while ensuring optimal matches between candidates and opportunities.

---
## Video Link
https://www.dropbox.com/scl/fi/yawgdepkkcgxikckb7spe/CS3200-Video.mov?rlkey=jt8ool7xdkzty1mcbpjmkeb7h&st=8ogw5585&dl=0

## Team Members
- **Yanzhen Chen** - Github usename: jasonchen1001 - committed to the development of front-end web pages and back-end functions for students and help teammates to revise the functions of school admin, HR and maintanence staff, and the production and modification of databases
- **Rongxuan Zhang** - Github usename: rxz991, RxZhang7 - committed to the development of front-end web pages and back-end functions for HR, and the production and modification of databases
- **Hanyun Cheng** - Github usename: AcceleratorBarry - committed to the development of front-end web pages and back-end functions for maintenance staff, and the production and modification of databases
- **Yiyang Bai** - Github usename: Ilovetheirishbeer - committed to the development of front-end web pages and back-end functions for school admin, and the production and modification of databases
- **Luke Kreysar** - Github usename: lukekrr - production and modification of database

---

## User Roles & Features

### 1. Student
**Pain Points:**
- Time constraints for tailoring resumes
- Lack of application feedback
- Difficulty tracking applications

**Features:**
- Resume upload and management
- Automated resume improvement suggestions
- Real-time application tracking
- View notification history
- Multiple resume versions support
- Application analytics dashboard

### 2. HR Manager
**Pain Points:**
- Overwhelming application volume
- Manual screening inefficiency

**Features:**
- Automated resume screening
- Custom filtering criteria
- Job posting management
- Recruitment analytics
- Automated candidate communication

### 3. School Administrator
**Pain Points:**
- Large volume student data management
- Compliance requirements

**Features:**
- Student record management
- Academic data updates
- Compliance reporting
- Data backup/recovery
- Performance analytics

### 4. Maintenance Staff
**Pain Points:**
- System update management
- Data integrity maintenance

**Features:**
- Database schema updates
- Security implementation
- Data cleanup tools
- System monitoring
- Backup management

---

## Technical Architecture

### Frontend
- **Streamlit framework**
- Responsive design
- Data visualization components

### Backend
- **Python Flask**
- RESTful API
- MySQL database
- Docker containerization


---

## Getting Started

Follow these steps to set up and run the InternMatch platform on your local machine.

---

### Prerequisites

Ensure the following tools are installed on your system:

- **Docker & Docker Compose**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop).  
  Verify installation with:
  ```bash
  docker compose version
  ```
- **Git**: Install [Git](https://git-scm.com/).  
  Verify installation with:
  ```bash
  git --version
  ```
- **Python 3.x**: Required for local development and running scripts.  
  Verify installation with:
  ```bash
  python --version
  ```

---

### Step 1: Clone the Repository

Clone the project repository using Git:

```bash
git clone https://github.com/jasonchen1001/24F-Project-Susy-Baka.git
cd 24F-Project-Susy-Baka
```

---

### Step 2: Configure Environment Variables

Create a `.env` file in the root directory of the project and add the following configuration:

```ini
SECRET_KEY=someCrazyS3cR3T!Key.!
DB_USER=root
DB_HOST=db
DB_PORT=3306
DB_NAME=project_susy_baka
MYSQL_ROOT_PASSWORD=123456
```

This file sets up environment variables required for secure database connections and application functionality.

---

### Step 3: Build and Start the Application

Build and start the application using Docker Compose:

```bash
docker compose up -d
```

This will:
- Set up a **MySQL database** on port `3306`.
- Start the **Flask API** backend on port `4000`.
- Launch the **Streamlit frontend** on port `8501`.

---

### Step 4: Verify Installation

To verify that all services are running correctly:

```bash
docker compose ps
```

You should see a list of running containers for the database, backend API, and frontend.

---

### Step 5: Access the Application

Open your browser and access the application at:

- **Frontend**: [http://localhost:8501](http://localhost:8501)  
- **API**: [http://localhost:4000](http://localhost:4000)


### Notes

- The first startup may take some time due to Docker image builds and database initialization.
- Regularly back up the database in production environments.
- Change all default credentials in the `.env` file for security.
- Use `docker logs <container-id>` to debug any issues during startup or runtime.

---
You are now ready to use InternMatch! If you encounter any issues, refer to the Troubleshooting section or contact the development team.