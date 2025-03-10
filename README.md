# Solution: Vendoring a Vulnerable Dependency

This walkthrough demonstrates how vendoring a dependency affects vulnerability scanning and dependency management. We'll scan for vulnerabilities in an installed package, identify the necessary function, locate its implementation, and then re-implement it manually.

## Step 1: Identify the Vulnerability

Before vendoring, let's check for vulnerabilities in the installed `requests` package.

### Scan with OSV-Scanner

If you haven't already installed OSV-Scanner, you can do so by following the [OSV-Scanner documentation](https://osv.dev/).

Run the following command to scan the dependencies:

```sh
osv-scanner scan -L requirements.txt
```

### Expected Output

The scanner should detect the vulnerability in `requests`:

```
✗ Vulnerability found in pip/requests (PyPI)
   Advisory: GHSA-9wx4-h78v-vm56  (CVE-2024-35195)
   Severity: MEDIUM
   Package: requests
   Version: 2.31.0
   Fixed in: 2.32.0
```

Now that we've identified the issue, let's replace `requests` by vendoring only the necessary functionality.

---

## Step 2: Find the Function and Re-Implement It

Instead of copying the entire `requests` library, we will identify the minimal functionality we need and manually recreate it.

### 1. Determine What Functionality You Need

Our code uses `requests.get()`, which performs an HTTP GET request.

To vendor this functionality, we must replace `requests.get()` with our own implementation.

### 2. Look Up the Implementation in `requests`

To correctly replace `requests.get()`, we need to understand how it works internally. We can do this by:

- Reading the official [Requests documentation](https://docs.python-requests.org/) to understand its behavior.
- Checking the source code by inspecting [requests' GitHub repository](https://github.com/psf/requests).
- Using Python's built-in help system to explore the function:

  ```python
  import requests
  help(requests.get)
  ```

  This will show that `requests.get()` is a wrapper around `requests.request("GET", ...)`.

- Locating the source code on your system:

  ```sh
  python -c "import requests; print(requests.__file__)"
  ```

  Open the printed file location and navigate to where `requests.get()` is implemented.

### 3. Replace the Functionality Using Built-in Libraries

Now that we understand `requests.get()`, we can re-implement it using `urllib`, a built-in Python module that performs HTTP requests. The next step is to manually write a function that behaves similarly to `requests.get()` but without the dependency.

**Important:** Do not simply copy-paste from `requests`. The goal is to extract only the necessary logic and implement a minimal, self-contained function.

```python
import urllib.request

def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req) as response:
        return response.read().decode()
```

---

## Step 3: Re-Scan the Project

Now that `requests` is no longer used, let's run OSV-Scanner again:

```sh
osv-scanner -r requirements.txt
```

### Expected Outcome

- The vulnerability is no longer detected, as `requests` is no longer present.
- The code is now self-contained, meaning future updates to `requests` won't affect it.
- Reachability is simplified, as we now have full control over the implementation.

---

## Conclusion

Vendoring the `requests` functionality by rewriting only what is needed has:

✔ Completely removed the vulnerable code from the project.  
✔ Eliminated false positives from security scans.  
✔ Ensured stability and maintainability by relying on built-in libraries.  
✔ Reduced reachability concerns, as the new implementation contains no unnecessary code.  

While vendoring isn't always the best solution, it's a powerful technique when dealing with dependency vulnerabilities. It allows you to take full control over your software, ensuring security and stability without external dependencies.

