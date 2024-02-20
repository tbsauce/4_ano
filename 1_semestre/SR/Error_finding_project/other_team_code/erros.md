# OverFlow
CWE-190: Integer Overflow or Wraparound

OWASP - "Memory Management" - "Check buffer boundaries if calling the function in a loop and protect against overflow"
### Explanation
Only 1st name needeed because it was too big and last name was dismissed.
Fgets and the developer didnt check for size, and buffer overflow.

![Alt text](/corrigir/img/image-1.png)

![Alt text](/corrigir/img/image-4.png)

# Bad memory free
CWE-401: Missing Release of Memory after Effective Lifetime

OWASP - "Memory Management" - "Properly free allocated memory upon the completion of functions and at all exit points"

### Explanation
Missing completely a free buf on getBlock

![Alt text](/corrigir/img/image-3.png)

# Bad input validation

CWE-20 : Improper Input Validation

OWASP - "Input validation" - "Validate data length"

### Explanation
The size of the input was never taken care of and the 
After the maximum of the funcion for input the rest of the chars that were in the input buffer weren't deleted.


![Alt text](/corrigir/img/image-2.png)
![Alt text](/corrigir/img/image.png)

# Null termination invalid

CWE-170: Improper Null Termination

OWASP - "Memory Management" - "When using functions that accept a number of bytes ensure that NULL terminatation is handled correctly"

### Explanation
The \0 is placed in the 16th postion it should be placed on the 15 since it starts on the 0.

![Alt text](/corrigir/img/image-5.png)