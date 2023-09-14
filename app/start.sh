#!/bin/bash
celery -A rate:celery call rate.run