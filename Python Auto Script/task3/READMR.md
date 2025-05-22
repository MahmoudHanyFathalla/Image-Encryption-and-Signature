# NIST Randomness Test Suite Analysis for Encrypted Images

## 1. Setting up the NIST Statistical Test Suite (STS)

The NIST Statistical Test Suite is a comprehensive package designed to test the randomness of binary sequences. Here's how to set it up on your virtual machine:

1. Download the NIST STS package from the Moodle link or from the NIST website.
2. Extract the package to your preferred directory.
3. Navigate to the extracted directory and compile the suite:
   ```
   cd sts-2.1.2
   make
   ```
4. Verify the installation was successful by running the sample tests.

## 2. Running Tests on the Original Image

To test the original image:

1. Convert your PNG image to a binary format suitable for NIST testing:
   - Extract the raw pixel data from your image
   - Convert it to a binary (0s and 1s) file, which is required for the NIST suite

2. Run the NIST suite against this binary file using:
   ```
   ./assess 1
   ```
   Then follow the prompts to select your input file and testing options.

3. Results for the original image will typically show low randomness scores, as natural images contain patterns, smooth color transitions, and structured content.

## 3. Running Tests on Encrypted Images

For each of your encrypted images (ECB, CBC, CFB, and OFB modes):

1. Extract the raw encrypted data from each file, excluding any headers.
2. Convert each to the binary format required by NIST STS.
3. Run the NIST suite against each encrypted file and collect the results.

## 4. Analysis of Results

When comparing the randomness test results:

### ECB Mode
- ECB (Electronic Codebook) typically performs the poorest in randomness tests
- Since ECB encrypts identical blocks of plaintext to identical blocks of ciphertext, patterns in the original image often remain visible in the encrypted version
- Results typically show failed frequency tests and other randomness indicators
- This is why ECB is generally not recommended for encrypting data with patterns, like images

### CBC Mode (Cipher Block Chaining)
- CBC introduces significantly better randomness than ECB
- Each block's encryption depends on all previous blocks, creating an avalanche effect
- The initialization vector (IV) ensures that identical plaintext blocks encrypt to different ciphertext blocks
- Expect high pass rates for most NIST tests

### CFB Mode (Cipher Feedback)
- CFB typically shows strong randomness properties
- Like CBC, it creates dependencies between blocks and uses an IV
- Works well for stream encryption needs
- Often performs similarly to CBC in randomness tests

### OFB Mode (Output Feedback)
- OFB generates a pseudo-random keystream independent of the plaintext
- Provides good randomness characteristics
- Since the keystream generation is separate from the encryption process, it can sometimes show slightly different randomness patterns than CBC/CFB

### Expected Ranking (Best to Worst Randomness):
1. CBC/CFB/OFB (often very close in performance)
2. ECB (significantly worse)

Generally, CBC, CFB, and OFB modes should all pass most NIST randomness tests with strong results, while ECB mode will likely fail several tests due to its preservation of patterns from the original image.

The specific test results to focus on include:
- Frequency Test (proportion of 0s and 1s)
- Runs Test (uninterrupted sequences of identical bits)
- Longest Run of Ones
- Binary Matrix Rank Test
- Approximate Entropy Test
- Cumulative Sums Test

Higher p-values in these tests (closer to 1.0) indicate better randomness. A mode that consistently produces p-values above the significance level (typically 0.01) across all tests would be considered to have achieved better randomness.