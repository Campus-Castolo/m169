# Define the necessary environment for the automated deployment of services.

**Essential Knowledge:**

## 1. Understands the fundamental principles of both monolithic and microservices architecture.

| **Principle**                                       | **Monolithic Architecture**                         | **Microservices Architecture**                       |
|-----------------------------------------------------|-----------------------------------------------------|-----------------------------------------------------|
| **Decomposition**                                   | Typically a single, unified codebase and database.  | Decomposed into smaller, independent services.       |
| **Scalability**                                     | Scaling involves replicating the entire application | Can scale individual services independently.         |
| **Development**                                     | Centralized development and deployment.              | Decentralized development and deployment.            |
| **Flexibility**                                     | Changes may require modifying the entire codebase. | Easier to make changes to specific services.         |
| **Fault Isolation**                                 | A failure can impact the entire system.              | Failures are contained within individual services.  |
| **Technology Stack**                                | Homogeneous technology stack.                        | Can use different technologies for different services.|
| **Communication**                                   | In-process communication between components.        | Inter-service communication through APIs.            |
| **Deployment**                                      | Deployed as a single unit.                           | Independent deployment of individual services.      |
| **Scalability**                                     | Vertical scaling (increasing resources of a single unit). | Horizontal scaling (adding more instances of specific services). |

**Monolithic Architecture:**<br>
Imagine you have a big LEGO castle. All the pieces of the castle, like the walls, towers, and doors, are connected together to make one huge castle. If you want to change something, like add a new tower, you have to touch the entire castle. It's like playing with a giant, single LEGO set where everything is stuck together.

**Microservices Architecture:**<br>
Now, think about having lots of smaller LEGO sets, each representing a different part of the castle - one for walls, another for towers, and so on. These sets can work together, but they are separate. If you want to change one part, like add a new tower, you only need to change that specific LEGO set without touching the rest. It's like building a big castle with many smaller, independent LEGO sets.

So, in simple terms:

- **Monolithic**: One big LEGO castle where all pieces are stuck together.
- **Microservices**: Many smaller LEGO sets, each representing a specific part, and they can work together to build something big.

## 2. Recognizes the key advantages and disadvantages of different architectures and demonstrates their impact on a service level (e.g., microservices architecture).

## 3. Knows the process of packaging services into containers.

## 4. Understands the procedures for deploying services in the backend and how these services are utilized in the frontend by clients.

## 5. Familiar with the underlying architecture of a container environment (Daemon, Client/Server, Images, Container, Registry).

## 6. Understands the dependencies of services and their deployment in a local infrastructure (examples: persistent data storage, networking, and others).