-- LAB_MEMBER
INSERT INTO lab_member (mid, name, join_date, type, mentor, m_sdate, m_edate) VALUES
(1, 'Maya Chen', '2022-08-20', 'student', NULL, NULL, NULL),
(2, 'Omar Patel', '2021-09-01', 'student', NULL, NULL, NULL),
(3, 'Elena Rodriguez', '2023-01-15', 'student', NULL, NULL, NULL),
(4, 'Noah Williams', '2020-08-25', 'student', NULL, NULL, NULL),
(5, 'Priya Nair', '2022-01-10', 'student', NULL, NULL, NULL),
(6, 'Lucas Brown', '2023-09-05', 'student', NULL, NULL, NULL),
(7, 'Dr. Aisha Rahman', '2016-07-01', 'faculty', NULL, NULL, NULL),
(8, 'Dr. Benjamin Lee', '2015-08-15', 'faculty', NULL, NULL, NULL),
(9, 'Dr. Carla Mendes', '2018-01-20', 'faculty', NULL, NULL, NULL),
(10, 'Dr. Daniel Kim', '2017-06-10', 'faculty', NULL, NULL, NULL),
(11, 'Dr. Evelyn Carter', '2014-09-01', 'faculty', NULL, NULL, NULL),
(12, 'Dr. Farah Ali', '2019-03-18', 'faculty', NULL, NULL, NULL),
(13, 'Grace Hopper Analytics', '2020-02-12', 'collaborator', NULL, NULL, NULL),
(14, 'Horizon BioSystems', '2021-04-30', 'collaborator', NULL, NULL, NULL),
(15, 'IonGrid Labs', '2019-11-05', 'collaborator', NULL, NULL, NULL),
(16, 'Jetstream Robotics', '2022-06-17', 'collaborator', NULL, NULL, NULL),
(17, 'Keystone Medical AI', '2023-02-22', 'collaborator', NULL, NULL, NULL),
(18, 'Lumen Materials Group', '2020-10-08', 'collaborator', NULL, NULL, NULL)
ON CONFLICT (mid) DO NOTHING;

-- STUDENT
INSERT INTO student (mid, sid, level, major) VALUES
(1, 'S1001', 'PhD', 'Computer Science'),
(2, 'S1002', 'MS', 'Data Science'),
(3, 'S1003', 'PhD', 'Biomedical Engineering'),
(4, 'S1004', 'BS', 'Computer Science'),
(5, 'S1005', 'MS', 'Electrical Engineering'),
(6, 'S1006', 'PhD', 'Data Science')
ON CONFLICT (mid) DO NOTHING;

-- COLLABORATOR
INSERT INTO collaborator (mid, affiliation, cv) VALUES
(13, 'Grace Hopper Analytics', 'https://example.com/cv/grace-hopper-analytics'),
(14, 'Horizon BioSystems', 'https://example.com/cv/horizon-biosystems'),
(15, 'IonGrid Labs', 'https://example.com/cv/iongrid-labs'),
(16, 'Jetstream Robotics', 'https://example.com/cv/jetstream-robotics'),
(17, 'Keystone Medical AI', 'https://example.com/cv/keystone-medical-ai'),
(18, 'Lumen Materials Group', 'https://example.com/cv/lumen-materials')
ON CONFLICT (mid) DO NOTHING;

-- FACULTY
INSERT INTO faculty (mid, department) VALUES
(7, 'Computer Science'),
(8, 'Data Science'),
(9, 'Biomedical Engineering'),
(10, 'Electrical Engineering'),
(11, 'Mechanical Engineering'),
(12, 'Materials Science')
ON CONFLICT (mid) DO NOTHING;

-- MENTORSHIP UPDATES
UPDATE lab_member SET mentor = 7, m_sdate = '2022-09-01' WHERE mid = 1;
UPDATE lab_member SET mentor = 8, m_sdate = '2021-09-15' WHERE mid = 2;
UPDATE lab_member SET mentor = 9, m_sdate = '2023-02-01' WHERE mid = 3;
UPDATE lab_member SET mentor = 7, m_sdate = '2020-09-01' WHERE mid = 4;
UPDATE lab_member SET mentor = 10, m_sdate = '2022-02-01' WHERE mid = 5;
UPDATE lab_member SET mentor = 8, m_sdate = '2023-09-15' WHERE mid = 6;
UPDATE lab_member SET mentor = 11, m_sdate = '2021-05-01' WHERE mid = 16;
UPDATE lab_member SET mentor = 12, m_sdate = '2020-11-01' WHERE mid = 18;

-- PROJECT
INSERT INTO project (pid, title, s_date, e_date, e_duration, leader) VALUES
(1, 'Adaptive Clinical NLP', '2023-01-10', '2028-12-31', '48 months', 7),
(2, 'Robotic Lab Automation', '2022-06-01', '2028-08-30', '51 months', 11),
(3, 'Privacy Preserving Genomics', '2024-02-01', '2029-01-31', '36 months', 9),
(4, 'Edge Sensor Networks', '2023-09-01', '2028-05-31', '33 months', 10),
(5, 'COVID Imaging Archive', '2020-04-01', '2021-12-31', '21 months', 9),
(6, 'Smart Campus Energy', '2019-01-15', '2022-05-30', '40 months', 10),
(7, 'Explainable Recommenders', '2020-09-01', '2023-03-31', '31 months', 8),
(8, 'Nanomaterial Failure Analysis', '2018-07-01', '2020-12-15', '30 months', 12)
ON CONFLICT (pid) DO NOTHING;

-- WORKS
INSERT INTO works (pid, mid, role, hours) VALUES
(1, 7, 'PI', 12),
(1, 1, 'Graduate RA', 20),
(1, 3, 'Graduate RA', 15),
(1, 17, 'Collaborator', 8),
(2, 11, 'PI', 10),
(2, 4, 'Undergraduate RA', 12),
(2, 16, 'Collaborator', 16),
(3, 9, 'PI', 12),
(3, 3, 'Graduate RA', 22),
(3, 6, 'Graduate RA', 18),
(3, 14, 'Collaborator', 10),
(4, 10, 'PI', 11),
(4, 5, 'Graduate RA', 20),
(4, 2, 'Graduate RA', 10),
(4, 15, 'Collaborator', 9),
(5, 9, 'PI', 8),
(5, 3, 'Graduate RA', 15),
(5, 13, 'Collaborator', 6),
(6, 10, 'PI', 9),
(6, 5, 'Graduate RA', 16),
(6, 12, 'Co-PI', 8),
(7, 8, 'PI', 10),
(7, 2, 'Graduate RA', 18),
(7, 1, 'Graduate RA', 12),
(7, 13, 'Collaborator', 7),
(8, 12, 'PI', 10),
(8, 18, 'Collaborator', 12),
(8, 6, 'Graduate RA', 8)
ON CONFLICT (pid, mid) DO NOTHING;

-- GRANT
INSERT INTO "grant" (gid, p_duration, agency, budget, start_date, pid) VALUES
(1, '24 months', 'NSF', 250000, '2023-01-01', 1),
(2, '18 months', 'NIH', 175000, '2024-03-01', 1),
(3, '36 months', 'DARPA', 420000, '2022-06-01', 2),
(4, '24 months', 'NIH', 300000, '2024-02-01', 3),
(5, '12 months', 'NJ Health Foundation', 85000, '2024-06-01', 3),
(6, '30 months', 'DOE', 210000, '2023-09-01', 4),
(7, '18 months', 'NSF', 125000, '2020-05-01', 5),
(8, '24 months', 'EPA', 95000, '2019-02-01', 6),
(9, '24 months', 'NSF', 150000, '2020-09-01', 7),
(10, '12 months', 'Industry Consortium', 50000, '2021-01-15', 7)
ON CONFLICT (gid) DO NOTHING;

-- EQUIPMENT
INSERT INTO equipment (eid, e_type, e_name, manual) VALUES
(1, 'GPU Server', 'A100 Compute Node', 'https://example.com/manuals/a100-node'),
(2, 'Microscope', 'Confocal Imaging System', 'https://example.com/manuals/confocal'),
(3, 'Robot Arm', 'UR5e Bench Robot', 'https://example.com/manuals/ur5e'),
(4, 'Sensor Kit', 'EdgeSense Kit', 'https://example.com/manuals/edgesense'),
(5, 'Sequencer', 'MiniSeq Platform', 'https://example.com/manuals/miniseq'),
(6, 'Storage', 'Research NAS', 'https://example.com/manuals/nas'),
(7, 'Workstation', 'Vision Workstation', 'https://example.com/manuals/vision-ws'),
(8, 'Power Meter', 'Campus Energy Meter', 'https://example.com/manuals/power-meter'),
(9, 'Thermal Chamber', 'Materials Thermal Chamber', 'https://example.com/manuals/thermal'),
(10, '3D Printer', 'Resin Prototype Printer', 'https://example.com/manuals/resin-printer'),
(11, 'Oscilloscope', 'Mixed Signal Scope', 'https://example.com/manuals/scope'),
(12, 'Wearable Kit', 'Clinical Wearable Sensors', 'https://example.com/manuals/wearables')
ON CONFLICT (eid) DO NOTHING;

-- DEVICE
INSERT INTO device (did, eid, status, p_date) VALUES
(1, 1, 'active', '2022-01-10'),
(2, 1, 'active', '2023-03-15'),
(3, 2, 'maintenance', '2020-07-20'),
(4, 2, 'active', '2021-05-12'),
(5, 3, 'active', '2022-08-01'),
(6, 3, 'inactive', '2019-11-30'),
(7, 4, 'active', '2023-09-10'),
(8, 4, 'active', '2023-09-10'),
(9, 5, 'maintenance', '2021-02-17'),
(10, 5, 'active', '2022-04-21'),
(11, 6, 'active', '2020-01-11'),
(12, 6, 'inactive', '2018-12-05'),
(13, 7, 'active', '2023-06-22'),
(14, 8, 'active', '2019-04-18'),
(15, 8, 'maintenance', '2020-09-09'),
(16, 9, 'active', '2018-08-08'),
(17, 10, 'inactive', '2021-12-12'),
(18, 10, 'active', '2024-01-15'),
(19, 11, 'active', '2020-10-10'),
(20, 12, 'active', '2023-02-28')
ON CONFLICT (did) DO NOTHING;

-- USES
INSERT INTO "uses" (mid, did, eid, s_date, e_date, purpose) VALUES
(1, 1, 1, '2023-02-01', NULL, 'NLP model training'),
(3, 2, 1, '2024-03-10', NULL, 'Genomics privacy experiments'),
(7, 1, 1, '2023-01-15', '2023-08-31', 'Clinical NLP baseline runs'),
(3, 4, 2, '2020-06-01', '2021-01-15', 'Imaging archive annotation'),
(9, 4, 2, '2020-04-15', '2021-12-15', 'Clinical imaging review'),
(4, 5, 3, '2022-09-01', NULL, 'Robot workflow testing'),
(16, 5, 3, '2022-09-15', NULL, 'Automation integration'),
(11, 5, 3, '2022-07-01', '2023-05-30', 'Robot calibration'),
(5, 7, 4, '2023-10-01', NULL, 'Edge sensor deployment'),
(2, 8, 4, '2023-11-05', NULL, 'Sensor data collection'),
(10, 7, 4, '2023-09-15', '2024-02-28', 'Network diagnostics'),
(3, 10, 5, '2024-04-01', NULL, 'Genome sequencing validation'),
(6, 10, 5, '2024-04-15', NULL, 'Variant analysis samples'),
(14, 9, 5, '2024-02-20', '2024-05-10', 'Protocol transfer'),
(1, 11, 6, '2023-03-01', NULL, 'Dataset storage'),
(2, 11, 6, '2021-10-01', '2023-03-30', 'Recommendation datasets'),
(13, 11, 6, '2020-10-01', '2022-12-20', 'Analytics archive'),
(6, 13, 7, '2024-05-01', NULL, 'Visualization workstation'),
(17, 13, 7, '2024-05-03', NULL, 'Clinical dashboard prototype'),
(5, 14, 8, '2019-03-15', '2022-05-01', 'Energy meter collection'),
(10, 14, 8, '2019-02-01', '2022-05-20', 'Energy model validation'),
(12, 16, 9, '2018-08-20', '2020-12-01', 'Thermal stress testing'),
(18, 16, 9, '2018-09-15', '2020-11-30', 'Materials failure analysis'),
(4, 18, 10, '2024-02-01', NULL, 'Robot gripper prototyping'),
(16, 18, 10, '2024-02-05', NULL, 'Prototype fixtures'),
(5, 19, 11, '2023-10-15', NULL, 'Signal validation'),
(10, 19, 11, '2023-10-01', '2024-04-01', 'Circuit diagnostics'),
(1, 20, 12, '2024-06-01', NULL, 'Clinical wearable pilot'),
(7, 20, 12, '2024-06-05', NULL, 'Study setup'),
(3, 3, 2, '2020-09-01', '2021-06-30', 'Microscopy review')
ON CONFLICT (mid, did, eid) DO NOTHING;

-- PUBLICATION
INSERT INTO publication (pubid, title, venue, date, doi) VALUES
(1, 'Clinical NLP Error Patterns', 'AMIA', '2020-03-15', '10.1000/rlm.2020.001'),
(2, 'Energy Forecasting for Smart Campuses', 'BuildSys', '2020-07-20', '10.1000/rlm.2020.002'),
(3, 'Thermal Stress in Nanomaterials', 'Materials Today', '2020-11-02', '10.1000/rlm.2020.003'),
(4, 'Imaging Archive Curation Methods', 'IEEE BHI', '2021-02-14', '10.1000/rlm.2021.004'),
(5, 'Confocal Pipelines for Clinical Imaging', 'MICCAI Workshop', '2021-06-18', '10.1000/rlm.2021.005'),
(6, 'Privacy Risks in Health Data Lakes', 'IEEE Security Workshops', '2021-10-03', '10.1000/rlm.2021.006'),
(7, 'Campus Energy Intervention Models', 'ACM e-Energy', '2022-01-25', '10.1000/rlm.2022.007'),
(8, 'Robotic Bench Automation Patterns', 'ICRA Workshop', '2022-04-12', '10.1000/rlm.2022.008'),
(9, 'Explainable Ranking for Research Search', 'RecSys', '2022-09-10', '10.1000/rlm.2022.009'),
(10, 'Sensor Fault Detection at the Edge', 'SenSys Workshop', '2022-12-01', '10.1000/rlm.2022.010'),
(11, 'Adaptive Clinical NLP Systems', 'ACL BioNLP', '2023-02-19', '10.1000/rlm.2023.011'),
(12, 'Human-in-the-Loop Lab Robotics', 'CASE', '2023-05-22', '10.1000/rlm.2023.012'),
(13, 'Mentee Collaboration Networks', 'JCDL', '2023-07-14', '10.1000/rlm.2023.013'),
(14, 'EdgeSense: Reliable Sensor Streams', 'IPSN', '2023-09-09', '10.1000/rlm.2023.014'),
(15, 'Fairness Audits for Clinical Models', 'FAccT Workshop', '2023-11-17', '10.1000/rlm.2023.015'),
(16, 'Private Genomic Similarity Search', 'RECOMB', '2024-01-30', '10.1000/rlm.2024.016'),
(17, 'Wearable Signals for Recovery Monitoring', 'NPJ Digital Medicine', '2024-03-08', '10.1000/rlm.2024.017'),
(18, 'Grant-Aware Project Planning', 'ICSE SEIS', '2024-05-11', '10.1000/rlm.2024.018'),
(19, 'Federated Lab Instrument Logs', 'VLDB Workshop', '2024-06-27', '10.1000/rlm.2024.019'),
(20, 'Multimodal Clinical Cohort Discovery', 'KDD Health Day', '2024-08-16', '10.1000/rlm.2024.020'),
(21, 'Robust Edge Networks for Labs', 'IEEE IoT Journal', '2025-01-10', '10.1000/rlm.2025.021'),
(22, 'Interpretable Genomic Privacy Metrics', 'Bioinformatics', '2025-02-28', '10.1000/rlm.2025.022'),
(23, 'Automation Scheduling with Human Oversight', 'Robotics and Automation Letters', '2025-04-04', '10.1000/rlm.2025.023'),
(24, 'Student-Led Clinical NLP Benchmarks', 'NAACL Findings', '2025-06-19', '10.1000/rlm.2025.024'),
(25, 'Materials Failure Prediction from Sparse Tests', 'Acta Materialia', '2025-09-05', '10.1000/rlm.2025.025')
ON CONFLICT (pubid) DO NOTHING;

-- PUBLISHES
INSERT INTO publishes (mid, pubid) VALUES
(7, 1),
(1, 1),
(10, 2),
(5, 2),
(12, 3),
(18, 3),
(9, 4),
(3, 4),
(13, 4),
(9, 5),
(3, 5),
(8, 6),
(2, 6),
(10, 7),
(5, 7),
(11, 8),
(4, 8),
(16, 8),
(8, 9),
(2, 9),
(1, 9),
(10, 10),
(5, 10),
(7, 11),
(1, 11),
(17, 11),
(11, 12),
(4, 12),
(16, 12),
(7, 13),
(1, 13),
(8, 13),
(10, 14),
(5, 14),
(15, 14),
(7, 15),
(3, 15),
(9, 16),
(3, 16),
(6, 16),
(7, 17),
(1, 17),
(17, 17),
(8, 18),
(2, 18),
(13, 18),
(6, 19),
(14, 19),
(9, 19),
(7, 20),
(1, 20),
(3, 20),
(10, 21),
(5, 21),
(15, 21),
(9, 22),
(6, 22),
(14, 22),
(11, 23),
(4, 23),
(16, 23),
(7, 24),
(1, 24),
(3, 24),
(12, 25),
(6, 25),
(18, 25)
ON CONFLICT (mid, pubid) DO NOTHING;

-- SEQUENCE RESETS
SELECT setval(pg_get_serial_sequence('lab_member', 'mid'), COALESCE((SELECT MAX(mid) FROM lab_member), 1), true);
SELECT setval(pg_get_serial_sequence('project', 'pid'), COALESCE((SELECT MAX(pid) FROM project), 1), true);
SELECT setval(pg_get_serial_sequence('"grant"', 'gid'), COALESCE((SELECT MAX(gid) FROM "grant"), 1), true);
SELECT setval(pg_get_serial_sequence('equipment', 'eid'), COALESCE((SELECT MAX(eid) FROM equipment), 1), true);
SELECT setval(pg_get_serial_sequence('device', 'did'), COALESCE((SELECT MAX(did) FROM device), 1), true);
SELECT setval(pg_get_serial_sequence('publication', 'pubid'), COALESCE((SELECT MAX(pubid) FROM publication), 1), true);
