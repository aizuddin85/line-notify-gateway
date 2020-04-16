# Line Notification Gateway #

Line Notification Gateway for Alertmanager OpenShift.

## Installation ##

# Docker build

```
# oc new-app https://github.com/aizuddin85/line-notify-gateway.git#master
```

# S2I build

```
oc new-build python:3.6~https://github.com/aizuddin85/line-notify-gateway.git#master
```


## Usage ##

Set receiver of generic webhook from Alertmanager.

```yaml
receivers:
  - name: 'line'
    webhook_configs:
      - url: 'http://webhook:5000/webhook'
        http_config:
          bearer_token: '« YOUR_LINE_API_TOKEN »'
```
