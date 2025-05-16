{{/* Return full name */}}
{{- define "microservices.fullname" -}}
{{ .Release.Name }}-{{ .Chart.Name }}
{{- end -}}