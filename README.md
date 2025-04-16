# 📞 VulcaNet Queue App
A simulated **Call Center Queue Management System** built in Python, using a **client-server architecture with Twisted**. Supports basic and advanced implementations with interactive command interface.
---

## 🚀 Features

- ✅ FIFO call queue logic;
- ✅ Operator state handling: `available`, `ringing`, `busy`;
- ✅ Client-server communication over TCP using JSON;
- ✅ Interactive terminal client (command-line);
- ✅ Multiple concurrent clients supported;
- ✅ Code fully documented and modular.


## ✨ Bonus Task <br/>

💎 Use twisted to read lines from stdin and call `Cmd.onecmd` as each line is read <br/>

## ⏩ Next Steps 

- Package the call center queue manager app as a container;
- Implement timeout detection.
---

## 🛠 Technologies Used

| Tool / Framework | Purpose |
|------------------|---------|
| 🐍 **Python 3** | Main programming language |
| 🔀 **Twisted** | Event-driven networking engine |
| 🧠 `cmd.Cmd` | Built-in command interpreter (client side) |
| 📦 `deque`, `json`, `protocol` | Standard Python modules |
| 🐧 **Linux / Bash** | Used via WSL and inside Docker containers |
| 🐳 **Docker** | Used to simulate a CentOS environment and isolate dependencies |
| 💻 **WSL (Windows Subsystem for Linux)** | Development environment on Windows |
| 🐙 [Git](https://git-scm.com/) | Version control for source code and collaboration |

---

## ▶️ How to Run

**🔧 Prerequisites** <br/>

- Python 3.8+ <br/>
- Docker (optional, for isolated environment)​ <br/>

**🐍 Running Locally**
1. Clone the repository (Code > SSH): `cd vulcanet`
2. Install dependencies: `pip install`
3. Start the server `python3 server.py`
4. In another terminal, start the client: `python3 client.py`

**🐳 Running with Docker**
1. Build the Docker image: `docker build -t vulcanet .`
2. Run the container: `docker run -it vulcanet`

## 💻 Supported Commands 

The client interface supports the following commands:​ <br/>
`call <caller_id>`: Enqueue a new caller. <br/>
`answer <operator_id>`: Operator answers the next call.<br/>
`hangup <operator_id>`: Operator ends the current call.<br/>
`status`: Display the current state of the queue and operators.<br/>
`help`: Show available commands.<br/>
`exit`: Exit the client application<br/>

## 👤 Author 
**Developed by Beatriz Moura, as part of the internship selection process for a Backend Developer role at VulcaNet.**
