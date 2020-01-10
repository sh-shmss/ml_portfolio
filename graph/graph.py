from nltk.data import find
import gensim
import math
# import networkx as nx
import numpy as np
from colour import Color
from bokeh.io import show
from bokeh.plotting import figure
from bokeh.models import GraphRenderer, StaticLayoutProvider, Circle, HoverTool, BoxZoomTool, ResetTool, Plot, Range1d
from bokeh.models import MultiLine
from bokeh.palettes import Spectral8
from bokeh.models.graphs import from_networkx

# word2vec_sample = str(find('models/word2vec_sample/pruned.word2vec.txt'))
# model = gensim.models.KeyedVectors.load_word2vec_format(word2vec_sample, binary=False)


class PlotNetwork:

    def __init__(self, word, n, model):
        self.n = n
        self.word = word
        self.model = model

    def find_similar_words(self, model, word, n):
        results = model.most_similar(positive=[word], topn=n)
        words = [words for words, _ in results]
        words.insert(0, word)
        return words

    def find_similar_weights(self, model, word, n):
        results = model.most_similar(positive=[word], topn=n)
        weights = [np.exp(weights) for _, weights in results]
        weights.insert(0, 0)
        return weights

    def make_plot(self):
        model, word, n = self.model, self.word, self.n
        G_words = self.find_similar_words(model, word, n)
        G_weights = self.find_similar_weights(model, word, n)

        N = len(G_words)
        node_indices = list(range(N))

        plot = figure(plot_width=500, plot_height=500,
                      x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1), tools="",
                      background_fill_color="white", x_axis_location=None,
                      y_axis_location=None,)
        plot.title.text = "Word Similarity Graph"
        plot.xgrid.visible = False
        plot.ygrid.visible = False
        node_hover_tool = HoverTool(tooltips=[("word", "@word")])
        plot.add_tools(node_hover_tool, BoxZoomTool(), ResetTool())

        graph = GraphRenderer()
        graph.node_renderer.data_source.add(node_indices, 'index')
        graph.node_renderer.data_source.add(G_words, 'word')
        graph.node_renderer.data_source.add(G_weights, 'weight')
        graph.node_renderer.glyph = Circle(size=15, fill_color="black")
        graph.edge_renderer.data_source.data = dict(
            start=[0] * N,
            end=node_indices)
        graph.edge_renderer.glyph = MultiLine(
            line_alpha=0.8, line_cap='square', line_dash='solid')

        red = Color("black")
        colors = list(red.range_to(Color("red"), N + 1))
        colors = [color.hex for color in colors]
        graph.edge_renderer.data_source.data["line_color"] = colors[1:]
        graph.edge_renderer.glyph.line_color = {'field': 'line_color'}

        graph.edge_renderer.data_source.data["line_width"] = G_weights
        graph.edge_renderer.glyph.line_width = {'field': 'line_width'}

        circ = [i * 2 * math.pi / N for i in node_indices]
        x = [math.cos(i) for i in circ]
        x[0] = 0.0
        y = [math.sin(i) for i in circ]
        y[0] = 0.65
        graph_layout = dict(zip(node_indices, zip(x, y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot.renderers.append(graph)

        return plot


#plot = PlotNetwork('school',50, model)
# plot.make_plot()
