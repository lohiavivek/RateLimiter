Command : python3 rate_limiter.py

3 endpoints:
1. http://127.0.0.1:5000/
2. http://127.0.0.1:5000/endpoint1
3. http://127.0.0.1:5000/endpoint2

Ratelimit config can be changed from rate_limit variable in rate_limiter.py

Curl command without user api key info : 
curl http://127.0.0.1:5000/

Curl command with user api key info : 
curl -H "X-Api-Key: client1" http://127.0.0.1:5000/


