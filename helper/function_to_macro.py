# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Pseudologic
# MAGIC
# MAGIC - Verify it is running in a dbt repo, e.g. search for a `dbt_project.yml`
# MAGIC - For all .sql files in the codebase, search for the existence of the fixed list of Snowflake functions
# MAGIC - For each function:
# MAGIC   - Verify it hasn't already been converted into a macro, e.g. ensure it isn't already preceded by `{{`
# MAGIC   - Replace the pattern `{function_name}({var1},{var2},...)` with `{{{function_name}("{var1}","{var2}",...)}}`
# MAGIC
# MAGIC   ## Progress
# MAGIC   
# MAGIC   Essentially works, now just need to create some Verification steps and make sure it can read all files in the repo!

# COMMAND ----------

import os
import re
from git import Repo

def toy_version(function_name):

    content = f"SELECT a, {function_name}(input1,input2) FROM table; SELECT b,{function_name}(blah,blah,blah2) FROM table 2"
    pattern = r'({}\()([^)]+)\)'.format(function_name)
    replacement = r'{{\1"\2")}}'
    
    updated_content = re.sub(pattern, replacement, content)
    matched_patterns = re.findall(pattern,updated_content)
    for i in matched_patterns:
      commas = r','
      quoted_commas = r'","'
      updated_match = re.sub(commas,quoted_commas,i[1])
      updated_content = updated_content.replace(i[1], updated_match)

    return updated_content

def find_replace_sql_files(repo_path, function_name):
    repo = Repo(repo_path)
    sql_files = repo.git.ls_files("*/*.sql").splitlines()

    pattern = r'({}\()([^)]+)\)'.format(function_name)
    replacement = r'{{\1"\2")}}'

    for file_path in sql_files:
        full_path = os.path.join(repo_path, file_path)

        with open(full_path, 'r+') as file:
            content = file.read()
            updated_content = re.sub(pattern, replacement, content)
            matched_patterns = re.findall(pattern,updated_content)
            for i in matched_patterns:
              commas = r','
              quoted_commas = r'","'
              updated_match = re.sub(commas,quoted_commas,i[1])
              updated_content = updated_content.replace(i[1], updated_match)

            file.seek(0)
            file.write(updated_content)
            file.truncate()

        print(f"Processed: {file_path}")

# COMMAND ----------

##Proving that the function works to create Macros from Functions
toy_version("array_agg")

# COMMAND ----------

input_functions = ["any_value"
,"approx_top_k"
,"approximate_count_distinct"
,"approximate_jaccard_index"
,"approximate_similarity"
,"array_agg"
,"array_append"
,"array_cat"
,"array_compact"
,"array_construct"
,"array_construct_compact"
,"array_insert"
,"array_intersection"
,"array_size"
,"array_slice"
,"array_to_string"
,"arrayagg"
,"as_char"
,"as_date"
,"as_integer"
,"as_number"
,"as_varchar"
,"base64_decode_binary"
,"base64_decode_string"
,"base64_encode"
,"bitand"
,"booland_agg"
,"boolor_agg"
,"boolxor_agg"
,"charindex"
,"check_json"
,"compress"
,"contains"
,"control.harmonize_compact"
,"convert_timezone"
,"date_from_parts"
,"dateadd"
,"dayname"
,"dayofweekiso"
,"decrypt"
,"div0"
,"editdistance"
,"encrypt"
,"endswith"
,"enrich_placement_ad_type"
,"equal_null"
,"get"
,"get_ddl"
,"get_path"
,"getdate"
,"hash_agg"
,"hex_decode_binary"
,"hex_decode_string"
,"hll"
,"hll_estimate"
,"hll_export"
,"hll_import"
,"iff"
,"ilike"
,"insert"
,"is_boolean"
,"is_date"
,"is_integer"
,"is_null_value"
,"is_real"
,"is_role_in_session"
,"json_extract_path_text"
,"last_query_id"
,"last_transaction"
,"len"
,"listagg"
,"md5_binary"
,"md5_hex"
,"md5_number_lower64"
,"md5_number_upper64"
,"median"
,"minhash"
,"minhash_combine"
,"mode"
,"monthname"
,"nullifzero"
,"object_agg"
,"object_construct"
,"object_delete"
,"object_insert"
,"object_keys"
,"objectagg"
,"parse_json"
,"parse_xml"
,"percentile_cont"
,"percentile_disc"
,"previous_day"
,"randstr"
,"ratio_to_report"
,"regexp"
,"regexp_count"
,"regexp_instr"
,"regexp_like"
,"regexp_substr"
,"seq1"
,"seq2"
,"seq4"
,"seq8"
,"sha1_hex"
,"sha2_binary"
,"sha2_hex"
,"split_part"
,"square"
,"st_intersects"
,"standardize"
,"startswith"
,"strtok"
,"strtok_to_array"
,"sysdate"
,"systimestamp"
,"time"
,"time_slice"
,"timeadd"
,"timediff"
,"timestamp_from_parts"
,"timestamp_ntz_from_parts"
,"timestampadd"
,"timestampdiff"
,"to_array"
,"to_binary"
,"to_boolean"
,"to_char"
,"to_number"
,"to_double"
,"to_geography"
,"to_decimal"
,"to_numeric"
,"to_object"
,"to_time"
,"to_timestamp_ltz"
,"to_timestamp_ntz"
,"to_timestamp_tz"
,"to_varchar"
,"to_variant"
,"truncate"
,"try_base64_decode_string"
,"try_cast"
,"try_parse_json"
,"try_to_binary"
,"try_to_boolean"
,"try_to_date"
,"try_to_decimal"
,"try_to_number"
,"try_to_numeric"
,"try_to_time"
,"try_to_timestamp"
,"try_to_timestamp_ntz"
,"try_to_timestamp_tz"
,"unicode"
,"uniform"
,"uuid_string"
,"variance_samp"
,"week"
,"weekiso"
,"xmlget"
,"yearofweek"
,"yearofweekiso"
,"zeroifnull"
]

# COMMAND ----------

for i in input_functions:
  find_replace_sql_files('git-path',i)

# COMMAND ----------



# COMMAND ----------


