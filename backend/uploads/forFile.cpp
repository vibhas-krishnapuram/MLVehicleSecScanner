#include <iostream>
#include <cstdlib>   // rand, srand
#include <ctime>
#include <sstream>

unsigned int weak_checksum(const std::string &s) {
    // Illustrative "weak checksum" using simple sum of bytes — NOT cryptographic
    unsigned int sum = 0;
    for (unsigned char c : s) sum += c;
    return sum;
}

int main() {
    // Weak RNG: using rand() seeded with fixed value (predictable).
    srand(1); // intentionally poor seed for detector; scanners should flag use of rand() for crypto.
    int r = rand();
    std::cout << "Weak RNG sample: " << r << std::endl;

    std::string payload = "telemetry_payload_example";
    unsigned int ck = weak_checksum(payload);
    std::cout << "Weak checksum: " << ck << std::endl;

    return 0;
}
