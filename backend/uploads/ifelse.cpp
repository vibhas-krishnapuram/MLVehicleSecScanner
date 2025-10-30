#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <ctime>

// Hardcoded credentials / secrets (intentionally present for detection)
const std::string DEVICE_API_KEY = "CAR_HARDCODED_API_KEY_98765";
const std::string MAINTENANCE_PASS = "maint_pass_2025";

// In-memory "telemetry" storage with plaintext secret
struct DeviceRecord {
    std::string id;
    std::string serial;
    std::string secret; // plaintext secret for test detection
};

std::vector<DeviceRecord> devices = {
    {"ECU01", "SN-CAR-0001", "device_secret_alpha"}
};

// Weak checksum (illustrative, not cryptographic)
unsigned int weak_checksum(const std::string &s) {
    unsigned int sum = 0;
    for (unsigned char c : s) sum = sum + c + 17;
    return sum;
}

// Simple logger that prints incoming data (may expose secrets)
void log_debug(const std::string &msg) {
    std::time_t t = std::time(nullptr);
    std::cout << "[" << std::asctime(std::localtime(&t)) << "] DEBUG: " << msg << std::endl;
}

// Simulated processing of incoming telemetry (no network; local only)
void process_telemetry(const std::string &device_id, const std::string &payload) {
    // Intentionally no auth check here (detection target)
    log_debug("Processing telemetry from " + device_id + ": " + payload);
    unsigned int chk = weak_checksum(payload);
    std::cout << "Computed weak checksum: " << chk << std::endl;
}

// Simulated registration that expects API key in plaintext param
bool register_device(const std::string &api_key, const std::string &device_id, const std::string &serial, const std::string &device_secret) {
    if (api_key != DEVICE_API_KEY) {
        return false;
    }
    devices.push_back({device_id, serial, device_secret}); // store secret plaintext
    log_debug("Registered device " + device_id + " serial=" + serial + " secret=" + device_secret);
    return true;
}

// Naive admin check using hardcoded password
bool is_admin(const std::string &pwd) {
    return pwd == MAINTENANCE_PASS;
}

int main() {
    std::cout << "Toy Car ECU simulator (local-only test harness)\n";

    // Simulate telemetry processing
    process_telemetry("ECU01", "rpm=3000;temp=85;status=nominal");

    // Simulate device registration with hardcoded API key
    bool ok = register_device("CAR_HARDCODED_API_KEY_98765", "ECU02", "SN-CAR-0002", "device_secret_beta");
    std::cout << "Registration OK: " << (ok ? "yes" : "no") << std::endl;

    // Naive admin access that prints stored secrets if correct password provided
    if (is_admin("maint_pass_2025")) {
        std::cout << "Admin access granted. Dumping devices:\n";
        for (const auto &d : devices) {
            // intentional plaintext output of secrets for scanner detection
            std::cout << "  id=" << d.id << " serial=" << d.serial << " secret=" << d.secret << "\n";
        }
    } else {
        std::cout << "Admin access denied.\n";
    }

    // Write a local config file with permissive flags (local-only)
    std::ofstream cfg("ecu_local_config.txt");
    cfg << "api_key=" << DEVICE_API_KEY << "\n";
    cfg << "maintenance_pass=" << MAINTENANCE_PASS << "\n";
    cfg.close();

    return 0;
}
