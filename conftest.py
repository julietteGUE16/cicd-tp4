"""Configuration pytest et Allure"""
import sys
from pathlib import Path

# Ajouter src au PYTHONPATH
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))