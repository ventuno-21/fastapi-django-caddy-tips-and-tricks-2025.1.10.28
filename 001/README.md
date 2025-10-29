### Simple fastapi project with using Caddy Load Balancer and Static File Server Configuration

This Caddyfile configures two local servers:  

http://localhost:3030  
 serves static files from /home/yas/caddy/static and proxies /api/* requests to two backend API   servers (127.0.0.1:8000 and 127.0.0.1:8001) using a round-robin load balancing policy with health   checks at /health.  

http://localhost:3031  
 serves a second static site from /home/yas/caddy/static2.  
Logs are stored in /home/yas/caddy/access.log for debugging and request analysis.  

ubuntu@DESKTOP-EHEFOG0:/home/yas/caddy/001$ tree
.
├── Caddyfile
├── README.md
├── access.log
├── app.py
├── app1.py
├── notes.txt
├── static
│   ├── 001.html
│   └── index.html
└── static2
    └── index.html


```
http://localhost:3030 {
```
This block defines a site that listens on port 3030 on localhost (your local machine).
Everything inside { ... } applies to requests made to http://localhost:3030.
---
```
    # static files path
    root * /home/yas/caddy/static
```
The root directive sets the root directory for static files.
That means when someone visits http://localhost:3030, Caddy will look for files inside:
---
```
/home/yas/caddy/static
```
This enables serving static files from the directory defined above.
So, Caddy becomes a simple file server (like Nginx’s autoindex or Apache’s default behavior).

Example:
If you have /home/yas/caddy/static/index.html,
it’ll be served when you open http://localhost:3030/.
---

```
    # api path
    handle_path /api/* {
```
This section handles all requests that start with /api/.
It isolates them so they’re not served as static files — instead, they’re sent to your backend (FastAPI, Django, etc.).
---
```
        reverse_proxy 127.0.0.1:8000 127.0.0.1:8001 {
```
This line sets up a reverse proxy — meaning:
Caddy receives the request, and then forwards it to one of your backend servers.
Here you have two backend instances running locally on port 8000 and port 8001.

So Caddy will balance (distribute) incoming API requests between these two backend servers.
---
```
            lb_policy round_robin 
```
lb_policy = load balancing policy  
round_robin means Caddy will send requests alternately to each backend:  

Copia codice  
1st request → 127.0.0.1:8000    
2nd request → 127.0.0.1:8001    
3rd request → back to 127.0.0.1:8000  
---
... and so on.
```
            health_uri /health
```
Caddy will periodically send a request to /health on each backend server to check if it’s alive.
If /health returns a success (like HTTP 200), that backend is considered healthy.
If not, Caddy will stop sending requests to it until it recovers.

Example:

If 127.0.0.1:8000/health fails → only 127.0.0.1:8001 will receive traffic.


---
```
    # log to investigate
    log {
        output file /home/yas/caddy/access.log
    }
```
This enables access logging.  
All incoming requests and their responses (status code, path, etc.) will be written to: 
```
/home/yas/caddy/access.log
```
Useful for debugging, monitoring, or analytics.
---

```
http://localhost:3031 {
    root * /home/yas/caddy/static2
    file_server
}
```
This defines another Caddy site on port 3031, separate from the first one.  
It serves static files from /home/yas/caddy/static2  
file_server makes those files publicly accessible.  

So you have:  

http://localhost:3030 → serves static files + proxies API requests   
http://localhost:3031 → serves another static directory independently  

✅ Summary:
Section	Purpose

| **Section** | **Purpose** |
|--------------|-------------|
| `http://localhost:3030` | Main site with static files + API proxy |
| `root * /home/yas/caddy/static` | Directory for static files |
| `handle_path /api/*` | Route `/api` requests to backend servers |
| `reverse_proxy 127.0.0.1:8000 127.0.0.1:8001` | Load balance between backend servers |
| `lb_policy round_robin` | Distribute requests evenly between backends |
| `health_uri /health` | Check backend health status |
| `log { output file ... }` | Save access logs for debugging and monitoring |
| `http://localhost:3031` | Second simple static site serving files from `/home/yas/caddy/static2` |

---

### ⚙️ Summary
- **Port 3030** → Main web app (static + API reverse proxy)  
- **Port 3031** → Secondary static site  
- **Load Balancing:** Round-robin between `:8000` and `:8001`  
- **Health Check:** Uses `/health` endpoint  
- **Logs:** Written to `/home/yas/caddy/access.log`