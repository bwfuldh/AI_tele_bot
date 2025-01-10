"""
PostgreSQL 데이터베이스 연결 및 쿼리 처리
심플한 구조로 분석 결과 저장/조회
"""

import os
import json
import psycopg2
from datetime import datetime
from psycopg2.extras import RealDictCursor

# 데이터베이스 URL
DATABASE_URL = os.getenv('DATABASE_URL')

def init_db():
    """데이터베이스 테이블 생성"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # analyses 테이블 생성
        cur.execute("""
            CREATE TABLE IF NOT EXISTS analyses (
                id SERIAL PRIMARY KEY,
                telegram_id TEXT,
                input_data JSONB,
                result JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        cur.close()
        conn.close()
        print("데이터베이스 초기화 성공")
    except Exception as e:
        print(f"데이터베이스 초기화 실패 (무시하고 계속 진행): {e}")

def save_analysis(telegram_id: str, input_data: dict, result: dict):
    """분석 결과 저장"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        cur.execute(
            """
            INSERT INTO analyses (telegram_id, input_data, result)
            VALUES (%s, %s, %s)
            """,
            (str(telegram_id), json.dumps(input_data), json.dumps(result))
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print("분석 결과 저장 성공")
    except Exception as e:
        print(f"분석 결과 저장 실패 (무시하고 계속 진행): {e}")

def get_user_analyses(telegram_id: str, limit: int = 5):
    """사용자의 최근 분석 결과 조회"""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute(
        """
        SELECT * FROM analyses 
        WHERE telegram_id = %s 
        ORDER BY created_at DESC 
        LIMIT %s
        """,
        (str(telegram_id), limit)
    )
    
    results = cur.fetchall()
    
    cur.close()
    conn.close()
    
    return results
