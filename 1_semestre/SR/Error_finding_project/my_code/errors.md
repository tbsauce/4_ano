# Bad encryption
CWE-327: Use of a Broken or Risky Cryptographic Algorithm

OWASP - "Cryptographic practices" - "Cryptographic modules used by the application should be compliant to FIPS 140-2 or an equivalent standard"

### Explanation
The Hash used on the password is valid for other use cases it shouldn't be used on the storage of information like passwords.

![Alt text](/impossivel/img/image.png)

# Input validation
CWE-75: Failure to Sanitize Special Elements into a Different Plane (Special Element Injection)

OWASP - "Input validation" - "Validate all client provided data before processing"

### Explanation
The function we created is not valid, because it doesn't sanitize all data, also "{}" this Brackets are not sanitizing the input meaning it is vulnerable to SQLi attacks.

![Alt text](/impossivel/img/image-1.png)

![Alt text](/impossivel/img/image-2.png)

![Alt text](/impossivel/img/image-4.png)

# Time based
CWE-208: Observable Timing Discrepancy

### Explanation
When acessing a user, if the user doen't exist the response is super fast. However acessing an existing user the time of response increased a lot.

![Alt text](/impossivel/img/image-3.jpeg)