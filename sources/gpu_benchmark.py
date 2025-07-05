import time
import moderngl
import moderngl_window as mglw
import numpy as np


def generate_grid_triangles(grid_size=100, quad_size=0.02):
    """
    Tworzy siatkę quadów, każdy quad to 2 trójkąty, razem 6 wierzchołków na quad.
    grid_size - liczba quadów w jednym wierszu/kolumnie
    quad_size - wielkość boku quada
    """
    vertices = []
    start = -1.0
    for y in range(grid_size):
        for x in range(grid_size):
            # pozycja lewego dolnego rogu quada
            x0 = start + x * quad_size
            y0 = start + y * quad_size
            x1 = x0 + quad_size
            y1 = y0 + quad_size

            # dwa trójkąty na quad
            vertices.extend([
                x0, y0,
                x1, y0,
                x0, y1,

                x1, y0,
                x1, y1,
                x0, y1,
            ])
    return np.array(vertices, dtype='f4')


class GPUStressTest(mglw.WindowConfig):
    # gl_version = (3, 3)
    title = "EffectiveMark V1.2 - GPU Render Test"
    window_size = (900, 850)
    resource_dir = "."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        vertex_shader = """
                #version 330
                in vec2 in_position;
                void main() {
                    gl_Position = vec4(in_position, 0.0, 1.0);
                }
                """

        fragment_shader = """
                #version 330
                out vec4 f_color;

                // Funkcja obciążająca GPU
                float heavyCalc(float x) {
                    float v = x;
                    for (int i = 0; i < 10000; i++) {
                        v = cos(log(v+1)) + sin(v*1.1) + abs(v)+1;

                    }
                    return v;
                }

                void main() {
                    float val = heavyCalc(gl_FragCoord.x * 0.01);
                    f_color = vec4(val, val * 0.5, 1.0 - val, 1.0);
                }
                """

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        vertices = generate_grid_triangles(grid_size=100, quad_size=0.02)
        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, "in_position")

        self.frame_count = 0
        self.start_time = time.perf_counter()
        self.test_duration = 10

    def on_render(self, time1: float, frame_time: float) -> None:
        global gpu_score
        self.ctx.clear(0.0, 0.0, 0.0)
        self.vao.render(mode=moderngl.TRIANGLES)

        self.frame_count += 1
        elapsed = time.perf_counter() - self.start_time
        if elapsed >= self.test_duration:
            fps = round(self.frame_count / elapsed, 1)
            # print(f"Benchmark zakończony! Średni FPS: {fps:.2f}")
            gpu_score = fps
            self.wnd.close()


def start_gpu_benchmark(): mglw.run_window_config(GPUStressTest)