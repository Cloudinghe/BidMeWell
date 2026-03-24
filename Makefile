# Makefile for Precision Bidding Project

.PHONY: help install test run validate clean

help:
	@echo "现代精确叫牌练习系统 - Makefile"
	@echo ""
	@echo "使用方法: make [目标]"
	@echo ""
	@echo "目标:"
	@echo "  install    安装依赖"
	@echo "  test       运行测试"
	@echo "  run        启动练习"
	@echo "  validate   验证规则"
	@echo "  clean      清理临时文件"
	@echo ""

install:
	pip install -r requirements.txt
	pip install -e .

test:
	python -m pytest tests/ -v

run:
	python scripts/run_practice.py

validate:
	python scripts/validate_rules.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
