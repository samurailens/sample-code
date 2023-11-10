## NZTA MotoCheck Java Project

This Java project provides a simple interface to interact with NZTA MotoCheck services, allowing you to authenticate a client and fetch vehicle details using Java.

## Prerequisites

1. Java 1.8 installed in system , with environment path set
2. External JAR files: saaj-api-1.3.5.jar and saaj-impl-1.3.8.jar (already included in the project)

# Installation

1. Clone the repository:
   https://github.com/Alamance-IT-Solution/sample-code.git
2. Navigate to the project directory:
   cd java

# Compiling the Code

1. Before compiling, remove the existing .class files:
   rm \*.class
2. Compile the Java file:
   javac -cp .:saaj-api-1.3.5.jar:saaj-impl-1.3.8.jar -source 1.8 -target 1.8 SOAPClientNZTA.java

# Running the Code

1. Execute the compiled Java file:
   java -cp .:saaj-api-1.3.5.jar:saaj-impl-1.3.8.jar SOAPClientNZTA
