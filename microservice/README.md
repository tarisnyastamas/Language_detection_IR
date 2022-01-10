# 1. Build container:
```bash
docker build -t language-detector-service .
```

# 2. Run container:
```bash
docker run -it \
    --rm \
    -p 5000:5000 \
    --env-file .env \
    --name language-detector-service
    language-detector-service
```

# 3. Send request:
Navigate to the following link in your browser
```
http://172.17.0.2:5000/detect/<your text here>?model='model_selection_string'
```

### Examples:
`http://172.17.0.2:5000/detect/this in english language?model=gradient_boost`<br>
`http://172.17.0.2:5000/detect/lets get out of here?model=decision_tree`

<br>

`model_selection_string`'s possible values are `gradient_boost`, `decision_tree` or you can leave it empty and the service is going to use the gradient boost model as the default.

