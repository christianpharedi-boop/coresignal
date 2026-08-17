# M0 Reproducibility Contract

A valid M0 result must record:
- experiment and protocol version;
- exact input source ID;
- raw and processed SHA-256 hashes;
- row count and date boundaries;
- chronological train/validation/test boundaries;
- model configuration;
- metrics in native units and milliseconds;
- execution timestamp;
- software revision;
- generated-output hashes.

The final test interval must never influence model selection.

M0 is a control experiment, not evidence of an inner-core mechanism.
