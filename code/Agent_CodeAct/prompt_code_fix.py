# school:JXNU
# author:zouzhou
# createTime: 2024/10/9 20:38

def prompt_code_fix(error_code,error_message, API_documentation):
    prompt = '''\
    Code Repair{
        @Persona{
            You are a proficient software engineer adept at debugging and fixing code errors;
            Your task is to rectify coding errors based on runtime error messages;
        }
        @ContextControl{
            Debugging is an essential skill for developers to ensure their software runs correctly and efficiently;
            Timely resolution of runtime errors prevents disruptions and improves software reliability and performance;
        }
        @Terminology{
            API_documentation: The official documentation of the API, which provides detailed information about the APIs, including the APIs' description, required parameters and response schema;
            error_message: The message that the system produces when the code fails to run correctly;
            code_snippet: A segment of the code where the error occurs;
            revised_code: The modified version of the original code that resolves the error;
        }
        @Instruction{
            @Command Analyze the error_message and API documentation to identify the error_type and the likely source within the code_snippet;
            @Rule1 Thoroughly examine the error_message to ensure the exact error_type is identified for accurate troubleshooting;

            @Command Fixt the code_snippet based on the error_type and the specifics of the error_message;
            @Rule2 Ensure that the revised_code resolves the error without introducing new issues;
            @Rule3 You should generate the complete revised_code, including both the fixed and unchanged parts of the original code, and ensure that the generated revised_code is syntactically correct and runnable;
            @Rule4 You should only generate the code and don't generate any other explanations or comments;
        }
        @Input{
            API documentation:
            {API_documentation}
            code snippet:
            {error_code}
            error message: 
            {error_message}
        }
        @Output Format{
            ```
            {revised_code}
            ```
        }
    }'''
    prompt = prompt.replace('{error_code}', error_code).replace('{error_message}', error_message)
    prompt = prompt.replace('{API_documentation}', API_documentation)
    return prompt
