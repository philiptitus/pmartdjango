from django.core.management.base import BaseCommand
from ecommerce.models import Product, Feature

# Map of product names to specialized features
PRODUCT_FEATURES = {
    "Mobile App Bug Fixing": [
        "Crash and ANR diagnostics with detailed reports",
        "Device and OS-specific issue resolution",
        "Regression testing and QA validation",
    ],
    "Push Notification Integration": [
        "Real-time push delivery with Firebase/OneSignal",
        "Segmented user targeting and scheduling",
        "Custom payloads and deep-linking support",
    ],
    "Create a Customized Mobile Application": [
        "Bespoke UI/UX design tailored to brand",
        "Integration with third-party APIs and services",
        "Offline data sync and local storage",
    ],
    "Chat & Messaging Features": [
        "Real-time messaging with WebSocket integration",
        "Typing indicators and read receipts",
        "Media (image/file) sharing and message encryption",
    ],
    "Landing Page Design & Development": [
        "Mobile-first responsive layouts",
        "Conversion-optimized call-to-actions",
        "Integration with analytics and lead capture",
    ],
    "Fix Website Bugs & Errors": [
        "Cross-browser compatibility fixes",
        "JavaScript and CSS debugging",
        "Performance optimization and error logging",
    ],
    "SEO Optimization": [
        "Structured data and schema markup",
        "Technical SEO audit and on-page fixes",
        "XML sitemap and robots.txt configuration",
    ],
    "Dark Mode & UI Enhancements": [
        "System theme detection and toggle",
        "Smooth animated transitions",
        "Accessibility and color contrast improvements",
    ],
    "AI-Powered Chatbot": [
        "NLP-powered intent recognition",
        "Context-aware multi-turn conversations",
        "Integration with external APIs and databases",
    ],
    "Data Scraping & Web Automation": [
        "Headless browser automation (Selenium/Playwright)",
        "Anti-bot and CAPTCHA bypass techniques",
        "Data export in CSV/JSON formats",
    ],
    "Deploy Web Apps on AWS/GCP/Azure": [
        "Automated CI/CD pipeline setup",
        "Infrastructure-as-Code deployment (Terraform)",
        "SSL, monitoring, and autoscaling configuration",
    ],
    "Setup CI/CD Pipelines": [
        "Multi-environment deployment workflows",
        "Automated testing and rollback strategies",
        "Integration with GitHub Actions/GitLab CI",
    ],
    "Cloud Database Setup": [
        "Secure provisioning of managed databases",
        "Automated backup and restore solutions",
        "Connection pooling and query optimization",
    ],
    "Docker & Kubernetes Setup": [
        "Dockerfile and Compose configuration",
        "Kubernetes deployment and scaling",
        "Service discovery and secrets management",
    ],
    "Payment Integrations": [
        "Stripe/PayPal API integration",
        "PCI DSS compliance and secure tokenization",
        "Subscription and one-time payment flows",
    ],
    "Subscription & Billing Systems": [
        "Automated recurring billing logic",
        "Invoice generation and email notifications",
        "Dunning management for failed payments",
    ],
    "Custom API Development": [
        "RESTful/GraphQL endpoint design",
        "JWT/OAuth2 authentication",
        "Rate limiting and API versioning",
    ],
    "AI API Integration": [
        "Integration with OpenAI/Gemini APIs",
        "Custom prompt engineering and response parsing",
        "Usage tracking and quota management",
    ],
    "Third-Party API Integration": [
        "OAuth2 and API key authentication",
        "Webhook handling and event-driven updates",
        "Error handling and retry logic",
    ],
    "OAuth & Social Login Integration": [
        "Google, Facebook, and GitHub login",
        "Secure token storage and refresh",
        "User profile data synchronization",
    ],
    "Microservices Architecture Setup": [
        "Service communication via gRPC/REST",
        "Centralized logging and monitoring",
        "API gateway and load balancing",
    ],
    "Create Custom AI Automations": [
        "Automated workflow orchestration",
        "ML model inference pipeline",
        "Trigger-based notifications and actions",
    ],
    "Tech Stack Recommendation Report": [
        "Comparative analysis of frameworks/tools",
        "Scalability and maintainability assessment",
        "Cost and performance benchmarking",
    ],
    "AI-Powered Marketing Automation": [
        "Automated campaign scheduling",
        "Lead scoring with machine learning",
        "Integration with CRM and email platforms",
    ],
}

class Command(BaseCommand):
    help = 'Delete all features and add unique, technical features to each product.'

    def handle(self, *args, **options):
        # Step 1: Delete all features
        Feature.objects.all().delete()
        self.stdout.write(self.style.WARNING('All existing features deleted.'))

        # Step 2: Add specialized features to each product
        updated_count = 0
        for product in Product.objects.all():
            features = PRODUCT_FEATURES.get(product.name)
            if features:
                for feature_text in features:
                    Feature.objects.create(product=product, text=feature_text)
                    self.stdout.write(self.style.SUCCESS(f'Added feature "{feature_text}" to "{product.name}"'))
                updated_count += 1
            else:
                self.stdout.write(self.style.ERROR(f'No feature mapping found for product: {product.name}'))
        self.stdout.write(self.style.SUCCESS(f'Features updated for {updated_count} products.'))
