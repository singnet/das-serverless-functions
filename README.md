# Documentation on DAS Serverless Functions

Serverless Functions represent an innovative approach to implementing and executing code in cloud computing environments. This architecture enables developers to create and execute code fragments in a granular manner, without concerns about the underlying infrastructure.

## OpenFaaS: Simplifying Serverless Functions Management

OpenFaaS, or Open Functions as a Service, is an open-source platform simplifying the entire life cycle of Serverless Functions. It provides a highly flexible and scalable framework for developing and executing functions in both cloud environments and local infrastructures.

### Obtaining Function Logs in faasd Using the `ctr` Command

To access logs from functions running in faasd, the `ctr` command offers a direct interface with containerd, responsible for managing containers in the system, such as faasd.

#### 1. Identifying the Function

The initial step involves identifying the name of the function from which logs are needed. Typically, this name corresponds to the container where the function is active. For instance, let's consider a function named `query-engine`.

#### 2. Using the `ctr` Command

Employ the `ctr` command to access logs from the desired function. Here's an example:

```bash
ctr -n openfaas-fn tasks exec --exec-id shell query-engine cat /var/log/das/das-query-engine.log
```

- `-n openfaas-fn`: Specifies the namespace in which the function is being executed in faasd.
- `tasks exec --exec-id shell query-engine`: Executes a command within the `query-engine` function's container.
- `cat /var/log/das/das-query-engine.log`: Command to display the contents of the `das-query-engine.log` log file.

#### 3. Viewing the Logs

After executing the command, the logs from the `query-engine` function will display in the terminal. If preferred, it's possible to redirect the output to a local file:

```bash
ctr -n openfaas-fn tasks exec --exec-id shell query-engine cat /var/log/das/das-query-engine.log > logs_query-engine.txt
```

Replace `logs_query-engine.txt` with the desired filename where you want to save the logs.
