#IMPORTSSSSSSS GANG HELL YEAH 
import sys
import os
import time
import math
import threading
import numpy as np
import scipy.ndimage as ndimage
#if you know me you know how much i love my COLOURSSSSSSSSSSSS
import colorama


#WHATS A CRANIUM 


class CranialDataSpace:
    @staticmethod
    def generate_high_fidelity_anatomy(dim=128):
        volume = np.zeros((dim, dim, dim), dtype=np.float32)
        z, y, x = np.ogrid[:dim, :dim, :dim]
        cx, cy, cz = dim / 2.0, dim / 2.0, dim / 2.0
        
        cortex_base = (((x - cx) / 46.0) ** 2 + ((y - (cy + 4.0)) / 56.0) ** 2 + ((z - cz) / 42.0) ** 2) <= 1.0
        volume[cortex_base] = 0.24
        
        outer_cortex_strip = (((x - cx) / 46.0) ** 2 + ((y - (cy + 4.0)) / 56.0) ** 2 + ((z - cz) / 42.0) ** 2)
        cortex_edge = (outer_cortex_strip <= 1.0) & (outer_cortex_strip >= 0.94)
        volume[cortex_edge] = 0.38
        
        sulci_noise = np.sin(x * 0.35) * np.cos(y * 0.35) * np.sin(z * 0.35)
        volume[cortex_base & (sulci_noise > 0.35)] *= 0.65
        
        ventricle_mask = (
            (((x - (cx - 9.0)) / 5.5) ** 2 + ((y - cy) / 24.0) ** 2 + ((z - (cz + 2.0)) / 7.0) ** 2 <= 1.0) |
            (((x - (cx + 9.0)) / 5.5) ** 2 + ((y - cy) / 24.0) ** 2 + ((z - (cz + 2.0)) / 7.0) ** 2 <= 1.0)
        )
        
        thalamus_mask = (
            (((x - (cx - 8.0)) / 8.5) ** 2 + ((y - (cy - 4.0)) / 12.0) ** 2 + ((z - (cz - 2.0)) / 10.0) ** 2 <= 1.0) |
            (((x - (cx + 8.0)) / 8.5) ** 2 + ((y - (cy - 4.0)) / 12.0) ** 2 + ((z - (cz - 2.0)) / 10.0) ** 2 <= 1.0)
        )
        
        cerebellum_mask = (((x - cx) / 32.0) ** 2 + ((y - (cy - 28.0)) / 20.0) ** 2 + ((z - (cz - 22.0)) / 16.0) ** 2) <= 1.0
        stem_mask = ((((x - cx) / 8.5) ** 2 + ((y - (cy - 10.0)) / 10.5) ** 2) <= 1.0) & (z < 46)
        
        volume[thalamus_mask & cortex_base] = 0.52
        volume[ventricle_mask] = 0.02
        volume[cerebellum_mask] = 0.32
        volume[stem_mask] = 0.26
        
        noise_grid = np.random.normal(0.0, 0.22, size=(dim, dim, dim)).astype(np.float32)
        smoothed_noise = ndimage.gaussian_filter(noise_grid, sigma=1.2)
        volume = np.where(volume > 0.0, volume + smoothed_noise * 0.15, 0.0)
        
        return np.clip(volume, 0.0, 1.0)

class StructuralSliceEngine:
    def __init__(self, volume_matrix):
        self.vol = volume_matrix
        self.dim = volume_matrix.shape[0]

    def render_voxel_slice(self, orientation, idx, anomaly=None):
        plane = np.zeros((self.dim, self.dim), dtype=np.float32)
        if orientation == "axial":
            plane[:, :] = self.vol[idx, :, :]
            if anomaly:
                ax, ay, az, weight, dev = anomaly
                y, x = np.ogrid[:self.dim, :self.dim]
                d = (x - ax)**2 + (y - ay)**2 + (idx - az)**2
                plane += np.exp(-d / (2.0 * (dev**2))) * weight
        elif orientation == "sagittal":
            plane[:, :] = self.vol[:, :, idx]
            if anomaly:
                ax, ay, az, weight, dev = anomaly
                z, y = np.ogrid[:self.dim, :self.dim]
                d = (idx - ax)**2 + (y - ay)**2 + (z - az)**2
                plane += np.exp(-d / (2.0 * (dev**2))) * weight
        elif orientation == "coronal":
            plane[:, :] = self.vol[:, idx, :]
            if anomaly:
                ax, ay, az, weight, dev = anomaly
                z, x = np.ogrid[:self.dim, :self.dim]
                d = (x - ax)**2 + (idx - ay)**2 + (z - az)**2
                plane += np.exp(-d / (2.0 * (dev**2))) * weight
        return np.clip(plane, 0.0, 1.0)
#uh
#science
#ye
#walter white yo 
#yo-yo





class RigorousNeuromorphicCore:
    def __init__(self, input_nodes=30, hidden_nodes=32, output_nodes=3):
        self.W1 = np.random.normal(1.0, 0.2, size=(hidden_nodes, input_nodes)).astype(np.float32)
        self.W2 = np.random.normal(1.0, 0.2, size=(output_nodes, hidden_nodes)).astype(np.float32)
        self.seu_counter = 0
        self.lock = threading.Lock()
        self.active = True

    def simulate_atmospheric_radiation(self, severity=0.75, latency_ms=25):
        while self.active:
            time.sleep(latency_ms / 1000.0)
            with self.lock:
                m1 = np.random.rand(*self.W1.shape) < (severity * 0.003)
                if np.any(m1):
                    self.W1[m1] = 0.0
                    self.seu_counter += np.sum(m1)
                m2 = np.random.rand(*self.W2.shape) < (severity * 0.003)
                if np.any(m2):
                    self.W2[m2] = 0.0
                    self.seu_counter += np.sum(m2)

class MathValidatedSpikingEngine:
    def __init__(self, hardware_instance, steps=50, dt_ms=1.0, tau_m_ms=20.0):
        self.hw = hardware_instance
        self.steps = steps
        self.dt = dt_ms
        self.decay_factor = np.exp(-self.dt / tau_m_ms, dtype=np.float32)
        self.v_threshold_base = 1.0
        self.thresholds = np.ones(32, dtype=np.float32) * self.v_threshold_base
        self.firing_traces = np.zeros(32, dtype=np.float32)
        self.tau_trace = 100.0
        self.target_activity = 0.20
        self.eta_homeostasis = 0.005
#guys why just why do we do classes
    def multidimensional_population_encode(self, norm_x, norm_y, norm_z, nodes_per_axis=10):
        total_nodes = nodes_per_axis * 3
        encoded_spikes = np.zeros((self.steps, total_nodes), dtype=np.float32)
        #SOOOOOOOOO MANY NODESSSSSSSSSSSSSSSSSS
        centers = np.linspace(0.0, 1.0, nodes_per_axis)
        sigma = 0.15
        
        act_x = np.exp(-((centers - norm_x) ** 2) / (2 * (sigma ** 2))) * 0.85
        act_y = np.exp(-((centers - norm_y) ** 2) / (2 * (sigma ** 2))) * 0.85
        act_z = np.exp(-((centers - norm_z) ** 2) / (2 * (sigma ** 2))) * 0.85
        unified_activations = np.concatenate([act_x, act_y, act_z])
        
        for t in range(self.steps):
            encoded_spikes[t] = np.random.rand(total_nodes) < unified_activations
        return encoded_spikes

    def process_frame(self, norm_x, norm_y, norm_z):
        spike_train = self.multidimensional_population_encode(norm_x, norm_y, norm_z, nodes_per_axis=10)
        
        v_hidden = np.zeros(self.hw.W1.shape[0], dtype=np.float32)
        v_output = np.zeros(self.hw.W2.shape[0], dtype=np.float32)
        output_spikes = np.zeros(self.hw.W2.shape[0], dtype=np.float32)
        
        with self.hw.lock:
            w1_snap = np.copy(self.hw.W1)
            w2_snap = np.copy(self.hw.W2)
            
        for t in range(self.steps):
            i_hidden = np.dot(w1_snap, spike_train[t])
            v_hidden = (v_hidden * self.decay_factor) + i_hidden
            
            fired_hidden = v_hidden >= self.thresholds
            v_hidden[fired_hidden] = 0.0
            
            self.firing_traces += (-self.firing_traces + fired_hidden.astype(np.float32)) * (self.dt / self.tau_trace)
            self.thresholds += self.eta_homeostasis * (self.firing_traces - self.target_activity)
            self.thresholds = np.clip(self.thresholds, 0.4, 2.5)
            
            i_output = np.dot(w2_snap, fired_hidden.astype(np.float32))
            v_output = (v_output * self.decay_factor) + i_output
            
            fired_output = v_output >= 1.0
            output_spikes += fired_output.astype(np.float32)
            v_output[fired_output] = 0.0
            
        return output_spikes

class PredictiveTrackingSystem:
    def __init__(self, origin_x=64.0, origin_y=64.0):
        self.State = np.array([[origin_x], [origin_y], [0.0], [0.0]], dtype=float)
        self.F = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]], dtype=float)
        self.H = np.array([[1,0,0,0],[0,1,0,0]], dtype=float)
        self.Covariance = np.eye(4) * 5.0
        self.Q_noise = np.eye(4) * 0.08
        self.R_noise = np.eye(2) * 0.55

    def filter_step(self, observation_x, observation_y):
        self.State = np.dot(self.F, self.State)
        self.Covariance = np.dot(np.dot(self.F, self.Covariance), self.F.T) + self.Q_noise
        
        measurement = np.array([[observation_x], [observation_y]], dtype=float)
        residual = measurement - np.dot(self.H, self.State)
        system_covariance = np.dot(np.dot(self.H, self.Covariance), self.H.T) + self.R_noise
        
        determinant = system_covariance[0,0] * system_covariance[1,1] - system_covariance[0,1] * system_covariance[1,0]
        inverse_sc = np.array([[system_covariance[1,1], -system_covariance[0,1]], [-system_covariance[1,0], system_covariance[0,0]]]) / (determinant if abs(determinant) > 1e-9 else 1.0)
        
        kalman_gain = np.dot(np.dot(self.Covariance, self.H.T), inverse_sc)
        self.State = self.State + np.dot(kalman_gain, residual)
        self.Covariance = np.dot(np.eye(4) - np.dot(kalman_gain, self.H), self.Covariance)
        return float(self.State[0,0]), float(self.State[1,0])

class AnatomicalTrueColorRasterizer:
    def _convert_density_to_rgb(self, structural_value):
        if structural_value <= 0.02:
            return 11, 13, 20
        elif structural_value <= 0.45:
            monochrome_scale = int(structural_value * 255.0 * 1.25)
            return min(255, monochrome_scale), min(255, monochrome_scale), min(255, monochrome_scale)
        else:
            deviation = (structural_value - 0.45) / 0.55
            red_channel = int(145 + (deviation * 110))
            green_channel = int(deviation * 230)
            blue_channel = int(20 - (deviation * 20))
            return min(255, red_channel), min(255, green_channel), max(0, blue_channel)

    def generate_teletext_viewport(self, mat, targets=None, step_factor=2):
        dy, dx = mat.shape
        lines = []
        
        for y in range(0, dy, step_factor * 2):
            chars = []
            for x in range(0, dx, step_factor):
                vt = mat[y, x]
                vb = mat[y + step_factor, x]
                
                rt, gt, bt = self._convert_density_to_rgb(vt)
                rb, gb, bb = self._convert_density_to_rgb(vb)
                
                if targets:
                    kx, ky = targets["k"]
                    mx, my = targets["m"]
                    if int(kx) == x and int(ky) == y:
                        chars.append(f"\033[38;2;0;255;0;48;2;{rb};{gb};{bb}m▀")
                        continue
                    if int(mx) == x and int(my) == y:
                        chars.append(f"\033[38;2;255;0;0;48;2;{rb};{gb};{bb}m▀")
                        continue
                        
                chars.append(f"\033[38;2;{rt};{gt};{bt};48;2;{rb};{gb};{bb}m▀")
            lines.append("".join(chars) + "\033[0m")
        return lines

class DiagnosticSystemCoordinator:
    def __init__(self):
        self.grid_dim = 128
        self.subject_id = "CTX-ALPHA-01"
        self.chemical_agent = "O15-RAD"
        self.injection_dosage = "40.0 mCi"
        self.total_frames = 120
        self.radiation_severity = 1.20

    def display_configuration_panel(self):
        sys.stdout.write("\033[H\033[2J")
        sys.stdout.flush()
        print(f"\033[1;31m" + "═"*154)
        print(f" SECURE INTERFACE: CORTICATWIN-128 STRUCTURAL NEURO-TELEMETRY WORKSPACE v12.3.0")
        print(f" MATHEMATICAL VALIDATION MODULE: POPULATION CODING & TIME-CONSTANT INVARIANCE ACTIVE")
        print(f"═"*154 + "\033[0m")
        
        id_in = input(" -> System Subject Registry Identifier [Default: CTX-ALPHA-01]: ")
        if id_in.strip(): self.subject_id = id_in.strip()
        
        iso_in = input(" -> Active Metabolic Radiation Tracer [Default: O15-RAD]: ")
        if iso_in.strip(): self.chemical_agent = iso_in.strip()
        
        dose_in = input(" -> Volumetric Injected Concentration Level (mCi) [Default: 40.0 mCi]: ")
        if dose_in.strip(): self.injection_dosage = dose_in.strip()
        
        fr_in = input(" -> Sequential Execution Frame Tracking Limit [Default: 120]: ")
        if fr_in.strip():
            try: self.total_frames = int(fr_in)
            except ValueError: self.total_frames = 120
            
        rad_in = input(" -> Cosmic Radiation Threat Severity Index (0.0 - 3.0) [Default: 1.20]: ")
        if rad_in.strip():
            try: self.radiation_severity = float(rad_in)
            except ValueError: self.radiation_severity = 1.20
        
        print("\n [SYSTEM-STATUS] Allocating high-fidelity volumetric spatial geometry matrix arrays...")
        self.anatomy_volume = CranialDataSpace.generate_high_fidelity_anatomy(self.grid_dim)
        #hmmmm i hate maths 
        self.scanner_core = StructuralSliceEngine(self.anatomy_volume)
        self.hardware_layer = RigorousNeuromorphicCore(input_nodes=30, hidden_nodes=32, output_nodes=3)
        self.neural_network = MathValidatedSpikingEngine(self.hardware_layer, steps=50, dt_ms=1.0, tau_m_ms=20.0)
        self.tracker = PredictiveTrackingSystem(64.0, 64.0)
        self.rasterizer = AnatomicalTrueColorRasterizer()
        time.sleep(1.0)

#BLEH:3#B
# #BLEH:3LEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3
#BLEH:3

#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
#BLEH:3
    def execute_live_imaging_stream(self):
        axial_z, sagittal_x, coronal_y = 60, 64, 64
        temporal_step = 0.0
        
        atmosphere = threading.Thread(
            target=self.hardware_layer.simulate_atmospheric_radiation, 
            kwargs={'severity': self.radiation_severity, 'latency_ms': 25}
        )
        atmosphere.daemon = True
        atmosphere.start()
        
        for frame in range(1, self.total_frames + 1):
            temporal_step += 0.20
            
            target_x = float(64.0 + 28.0 * math.sin(temporal_step * 0.70))
            target_y = float(64.0 + 24.0 * math.cos(temporal_step * 0.50))
            target_z = float(56.0 + 15.0 * math.sin(temporal_step * 1.05))
            
            output_spikes = self.neural_network.process_frame(target_x/128.0, target_y/128.0, target_z/128.0)
            
            metabolic_expansion_factor = 0.40 + (np.sum(output_spikes) / 130.0)
            anomaly_signature = (target_x, target_y, target_z, metabolic_expansion_factor, 7.5)
            
            axial_matrix = self.scanner_core.render_voxel_slice("axial", axial_z, anomaly_signature)
            sag_matrix = self.scanner_core.render_voxel_slice("sagittal", sagittal_x, anomaly_signature)
            cor_matrix = self.scanner_core.render_voxel_slice("coronal", coronal_y, anomaly_signature)
            
            measured_x = target_x + np.random.normal(0.0, 1.45)
            measured_y = target_y + np.random.normal(0.0, 1.45)
            
            kalman_x, kalman_y = self.tracker.filter_step(measured_x, measured_y)
            
            axial_targets = {"k": (kalman_x, kalman_y), "m": (measured_x, measured_y)}
            sag_targets = {"k": (target_y, target_z), "m": (target_y, target_z)}
            cor_targets = {"k": (kalman_x, target_z), "m": (measured_x, target_z)}
            
            axial_lines = self.rasterizer.generate_teletext_viewport(axial_matrix, axial_targets, step_factor=2)
            sagittal_lines = self.rasterizer.generate_teletext_viewport(sag_matrix, sag_targets, step_factor=2)
            coronal_lines = self.rasterizer.generate_teletext_viewport(cor_matrix, cor_targets, step_factor=2)
            
            sys.stdout.write("\033[H")
            print(f"\033[1;41m\033[1;37m" + " "*154 + "\033[0m")
            print(f"  CORTICATWIN-128: HIGH-DENSITY CRANIAL TELEMETRY SCANNER LAYER — REAL TIME STRUCTURAL ARRAYS     \033[0m")
            print(f"\033[1;41m\033[1;37m" + " "*154 + "\033[0m")
            print(f" \033[1;31m[REGISTRY ID]:\033[0m {self.subject_id:<16} | \033[1;31m[TRACER]:\033[0m {self.chemical_agent:<10} | \033[1;31m[DOSAGE]:\033[0m {self.injection_dosage:<8} | \033[1;31m[FRAME INTERVAL]:\033[0m {frame:03d}/{self.total_frames:03d}")
            print(f"\033[1;30m" + "─"*154 + "\033[0m")
            print(f"      AXIAL TRANSVERSE VIEW (Z: {axial_z:03d})               SAGITTAL PROFILE VIEW (X: {sagittal_x:03d})               CORONAL BACKPLANE VIEW (Y: {coronal_y:03d})")
            print(f"   ┌" + "─"*32 + "┐         ┌" + "─"*32 + "┐         ┌" + "─"*32 + "┐")
            
            for line_index in range(32):
                print(f"   │{axial_lines[line_index]}│         │{sagittal_lines[line_index]}│         │{coronal_lines[line_index]}│")
                
            print(f"   └" + "─"*32 + "┘         └" + "─"*32 + "┘         └" + "─"*32 + "┘")
            
            with self.hardware_layer.lock:
                unallocated_elements = (self.hardware_layer.W1 == 0.0).sum() + (self.hardware_layer.W2 == 0.0).sum()
                total_elements = self.hardware_layer.W1.size + self.hardware_layer.W2.size
            corruption_percentage = (unallocated_elements / total_elements) * 100.0
            
            print(f"\033[1;30m" + "─"*154 + "\033[0m")
            print(f"  \033[1;32m[EMERALD GREEN - KALMAN ESTIMATION]:\033[0m ({kalman_x:.2f}, {kalman_y:.2f})  |  \033[1;31m[RIGOROUS RADIATION DAMAGE]:\033[0m {self.hardware_layer.seu_counter} SEU Blips")
            print(f"  \033[1;31m[NEON RED - TRACKED TRANSVERSE NODES]:\033[0m ({measured_x:.2f}, {measured_y:.2f})  |  \033[1;33m[SMOOTH HOMEOSTATIC MEAN V_TH]:\033[0m {np.mean(self.neural_network.thresholds):.3f}V")
            print(f"\033[1;31m" + "═"*154 + "\033[0m")
            time.sleep(0.05)
            
        self.hardware_layer.active = False

if __name__ == "__main__":
    coordinator = DiagnosticSystemCoordinator()
    coordinator.display_configuration_panel()
    coordinator.execute_live_imaging_stream()
#signed KDS112301 OR krishndev EEYA EEYA YAY YE YAY YE
#please spare change spare change
#t³ would be proud of ts 
#arf arf arf arf arf im a sea lion   arf arf arf ououououououououo
