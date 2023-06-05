{{/*
Expand the name of the chart.
*/}}
{{- define "reddvid-backend.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "reddvid-backend.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "reddvid-backend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "reddvid-backend.labels" -}}
helm.sh/chart: {{ include "reddvid-backend.chart" . }}
{{ include "reddvid-backend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "reddvid-backend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "reddvid-backend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Pod annotations
*/}}
{{- define "reddvid-backend.pod.annotations" -}}
{{- range $k, $v := .Values.podAnnotations }}
{{- $k }}: {{ $v }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
checksum: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
{{- end }}

{{/*
Service annotations
*/}}
{{- define "reddvid-backend.service.annotations" -}}
prometheus/scrape: {{ .Values.service.prometheus.enabled | quote }}
{{- range $k, $v := .Values.service.annotations }}
{{- $k }}: {{ $v }}
{{- end }}
{{- if .Values.service.prometheus.enabled }}
prometheus.io/scheme: {{ .Values.service.prometheus.scheme | quote}}
prometheus.io/path: {{ .Values.service.prometheus.path | quote}}
prometheus.io/port: {{ .Values.service.prometheus.port | quote}}
{{- end }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "reddvid-backend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "reddvid-backend.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
