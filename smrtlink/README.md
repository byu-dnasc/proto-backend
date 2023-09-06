### Get auth token using curl
```
API_USER = ''
API_PASS = ''
AUTH_TOKEN=$(curl -k -s --user KMLz5g7fbmx8RVFKKdu0NOrJic4a:6NjRXBcFfLZOwHc0Xlidiz4ywcsa -d 'grant_type=password&username=$API_USER&password=$API_PASS&scope=sample-setup+run-design+run-qc+data-management+analysis+userinfo+openid' https://smrt.rc.byu.edu:8243/token | ~/jq -r .access_token)
```

### Make API call using curl and auth token
curl -k -s -H 'Authorization: Bearer $AUTH_TOKEN' http://localhost:9091/smrt-link/project