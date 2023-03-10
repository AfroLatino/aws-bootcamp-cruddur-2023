from datetime import datetime, timedelta, timezone
from opentelemetry import trace
import logging

from lib.db import pool, query_wrap_array

tracer = trace.get_tracer("home.activities")

class HomeActivities:
  def run(cognito_user_id=None): 
     # logger.info("HomeActivities")
    ## HoneyComb Span addition
    #with tracer.start_as_current_span("http-handler") as outer_span:
    #    outer_span.set_attribute("http-handler", True)
    #with tracer.start_as_current_span("home-activities-mock-data"):
      #span = trace.get_current_span()
      #now = datetime.now(timezone.utc).astimezone()
      #span.set_attribute("user.id", 'AfroLatino')
      #span.set_attribute("app.now", now.isoformat())  

      sql = query_wrap_array("""
      SELECT
        activities.uuid,
        users.display_name,
        users.handle,
        activities.message,
        activities.replies_count,
        activities.reposts_count,
        activities.likes_count,
        activities.reply_to_activity_uuid,
        activities.expires_at,
        activities.created_at
      FROM public.activities
      LEFT JOIN public.users ON users.uuid = activities.user_uuid
      ORDER BY activities.created_at DESC   
      """)
      print("SQL----------")
      print("sql")
      print("SQL----------")
      with pool.connection() as conn:
        with conn.cursor() as cur:
          cur.execute(sql)

          json = cur.fetchone()
      return json[0]
      return results
  