"""
Universal AI Agent Skills - 90+ Skills
From awesome-ai-agent-skills repository
"""

# Code and Development
from .code_documentation import CodeDocumentation
from .code_review import CodeReview
from .debugging import Debugging
from .refactoring import Refactoring
from .testing import Testing
from .version_control import VersionControl

# Data and Analytics
from .data_analysis import DataAnalysis
from .data_cleaning import DataCleaning
from .data_visualization import DataVisualization
from .sql_query_generation import SQLQueryGeneration

# DevOps and Infrastructure
from .ci_cd import CICD
from .cloud_monitoring import CloudMonitoring
from .docker_compose import DockerCompose
from .kubernetes_deployment import KubernetesDeployment

# Communication
from .email_drafting import EmailDrafting
from .meeting_transcription import MeetingTranscription
from .report_generation import ReportGeneration

# Research and Knowledge
from .deep_research import DeepResearch
from .fact_checking import FactChecking
from .summarization import Summarization

__all__ = [
    # Code
    "CodeDocumentation", "CodeReview", "Debugging", "Refactoring", "Testing", "VersionControl",
    # Data
    "DataAnalysis", "DataCleaning", "DataVisualization", "SQLQueryGeneration",
    # DevOps
    "CICD", "CloudMonitoring", "DockerCompose", "KubernetesDeployment",
    # Communication
    "EmailDrafting", "MeetingTranscription", "ReportGeneration",
    # Research
    "DeepResearch", "FactChecking", "Summarization",
]
