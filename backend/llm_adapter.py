"""
LLM API adapters for EduInsight-AI.

This module provides pluggable adapters for different LLM providers.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class LLMAdapter(ABC):
    """Abstract base class for LLM API adapters."""

    @abstractmethod
    async def generate_completion(
        self, prompt: str, system_message: Optional[str] = None
    ) -> str:
        """Generate a completion based on the provided prompt."""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Return the name of the model being used."""
        pass


class MockLLMAdapter(LLMAdapter):
    """Mock LLM adapter for testing and demonstration."""

    def __init__(self):
        self.model_name = "mock-llm-v1"

    async def generate_completion(
        self, prompt: str, system_message: Optional[str] = None
    ) -> str:
        """Generate a mock response for testing purposes."""
        # This simulates what a real LLM would return
        return """## Student Overview

The student demonstrates a developing understanding of the current curriculum with some foundational concepts in place.

## Academic Performance

Recent assessments indicate areas requiring additional instructional support, particularly in problem-solving and multi-step reasoning.

## Knowledge Point Analysis

### Weak Areas
- Understanding word problems
- Multi-step linear equations

### Stable Areas
- Basic arithmetic operations
- Simple ratio and proportion

## Common Learning Issues

- Calculation errors when transposing terms
- Conceptual confusion between ratios and fractions
- Over-reliance on memorized examples

## Learning Behavior Insights

- Homework completed on time
- Low classroom participation
- Limited self-review of mistakes

## Teaching Suggestions

1. Use structured problem-solving frameworks
2. Encourage verbalization of reasoning steps
3. Provide guided practice with increasing complexity
4. Reinforce correct reasoning over final answers
5. Offer positive feedback to build confidence

## Study Suggestions

1. Break word problems into smaller logical steps
2. Recheck calculations after each step
3. Review incorrect answers with explanations
4. Focus on understanding principles rather than memorization

---

*This analysis is AI-generated for instructional support only. Final teaching decisions should be made by teachers based on professional judgment.*"""

    def get_model_name(self) -> str:
        return self.model_name


class OpenAIAdapter(LLMAdapter):
    """OpenAI API adapter."""

    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _get_client(self):
        """Lazy initialization of the OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncOpenAI

                self._client = AsyncOpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError(
                    "Please install openai package: pip install openai"
                )
        return self._client

    async def generate_completion(
        self, prompt: str, system_message: Optional[str] = None
    ) -> str:
        """Generate completion using OpenAI API."""
        client = self._get_client()

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.7
        )

        return response.choices[0].message.content

    def get_model_name(self) -> str:
        return f"openai-{self.model}"


class AzureOpenAIAdapter(LLMAdapter):
    """Azure OpenAI Service adapter."""

    def __init__(
        self,
        api_key: str,
        azure_endpoint: str,
        api_version: str = "2024-02-15-preview",
        model: str = "gpt-35-turbo",
    ):
        self.api_key = api_key
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version
        self.model = model
        self._client = None

    def _get_client(self):
        """Lazy initialization of the Azure OpenAI client."""
        if self._client is None:
            try:
                from openai import AsyncAzureOpenAI

                self._client = AsyncAzureOpenAI(
                    api_key=self.api_key,
                    azure_endpoint=self.azure_endpoint,
                    api_version=self.api_version,
                )
            except ImportError:
                raise ImportError(
                    "Please install openai package: pip install openai"
                )
        return self._client

    async def generate_completion(
        self, prompt: str, system_message: Optional[str] = None
    ) -> str:
        """Generate completion using Azure OpenAI API."""
        client = self._get_client()

        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": prompt})

        response = await client.chat.completions.create(
            model=self.model, messages=messages, temperature=0.7
        )

        return response.choices[0].message.content

    def get_model_name(self) -> str:
        return f"azure-{self.model}"


def create_llm_adapter(
    provider: str, **kwargs
) -> LLMAdapter:
    """
    Factory function to create an LLM adapter based on provider.

    Args:
        provider: The LLM provider name ('mock', 'openai', 'azure')
        **kwargs: Provider-specific arguments

    Returns:
        An instance of LLMAdapter
    """
    providers = {
        "mock": MockLLMAdapter,
        "openai": OpenAIAdapter,
        "azure": AzureOpenAIAdapter,
    }

    if provider not in providers:
        raise ValueError(
            f"Unknown provider: {provider}. Available: {list(providers.keys())}"
        )

    return providers[provider](**kwargs)
