{{/* vim: set filetype=mustache: */}}

{{/*
Common labels
*/}}
{{- define "app.labels" -}}
app: {{ .Values.app }}
env: {{ .Values.labels.env }}
{{- end -}}

{{/*
Resources
*/}}
{{- define "app.resources" -}}
resources:
  limits:
    cpu: {{ .Values.resources.limits.cpu }}
    memory: {{ .Values.resources.limits.memory }}
  requests:
    cpu: {{ .Values.resources.requests.cpu }}
    memory: {{ .Values.resources.requests.memory }}
{{- end -}}

{{/*
Affinity
*/}}
{{- define "app.podAntiAffinity" -}}
podAntiAffinity:
  preferredDuringSchedulingIgnoredDuringExecution:
    - weight: 100
      podAffinityTerm:
        labelSelector:
          matchExpressions:
            - key: app
              operator: In
              values:
                - {{ .Values.app }}
        topologyKey: "kubernetes.io/hostname"
{{- end -}}

{{- define "app.nodeAffinity" -}}
{{- if eq .Values.labels.env "avilabs-dev" -}}
nodeAffinity:
  requiredDuringSchedulingIgnoredDuringExecution:
    nodeSelectorTerms:
      - matchExpressions:
          - key: node.kubernetes.io/node-type
{{- if eq .Values.version "master" }}
            operator: In
{{- else }}
            operator: NotIn
{{- end }}
            values:
              - on-demand
{{- end -}}
{{- end -}}
