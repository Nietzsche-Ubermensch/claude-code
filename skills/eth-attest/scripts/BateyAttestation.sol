// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * BateyAttestation — On-chain registry for PQC-signed document attestations.
 * Each attestation records the SHA3-512 hash of a document signed with
 * ML-DSA-87 (FIPS 204) and SPHINCS+-SHAKE-256s (FIPS 205).
 * Records are immutable once written.
 */
contract BateyAttestation {

    struct Attestation {
        string  attestation_id;
        string  document;
        string  author;
        string  sha3_512;
        uint256 block_timestamp;
    }

    mapping(string => Attestation) private _records;
    mapping(string => bool)        private _exists;
    string[] public ids;

    event AttestationRegistered(
        string indexed attestation_id,
        string  document,
        string  author,
        string  sha3_512,
        uint256 block_timestamp
    );

    /// @notice Register a new attestation. Reverts if already registered.
    function register(
        string calldata attestation_id,
        string calldata document,
        string calldata author,
        string calldata sha3_512
    ) external {
        require(!_exists[attestation_id], "Already registered");
        _records[attestation_id] = Attestation(attestation_id, document, author, sha3_512, block.timestamp);
        _exists[attestation_id]  = true;
        ids.push(attestation_id);
        emit AttestationRegistered(attestation_id, document, author, sha3_512, block.timestamp);
    }

    /// @notice Look up an attestation by ID.
    function get(string calldata attestation_id) external view returns (Attestation memory) {
        require(_exists[attestation_id], "Not found");
        return _records[attestation_id];
    }

    /// @notice Total number of registered attestations.
    function count() external view returns (uint256) {
        return ids.length;
    }
}
