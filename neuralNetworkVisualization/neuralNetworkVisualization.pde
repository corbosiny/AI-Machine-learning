int backgroundColor = 255;
int textColor = 0;

float weights[] = {2, -2};
float weights2[] = {1,2,1};
float weights3[] = {4,2,-3,7,2};
float weights4[] = {-4, -3, -4, -1, -2};
float inputs[][] = {{-5,-4}, {8,-20}, {4,7}};

NeuralNet net;
void setup()
{
  size(500, 500);
  surface.setResizable(true);;
  Perceptron newNeuron = new Perceptron(weights);;
  Perceptron newNeuron2 = new Perceptron(weights);;
  Perceptron newNeuron3 = new Perceptron(weights);;
  Perceptron newNeurons[] = {newNeuron, newNeuron2, newNeuron3};
  NeuronLayer newLayer = new NeuronLayer(newNeurons);
  
  Perceptron newNeuron4 = new Perceptron(weights2);
  Perceptron newNeuron5 = new Perceptron(weights2);
  Perceptron newNeuron6 = new Perceptron(weights2);
  Perceptron newNeuron7 = new Perceptron(weights2);
  Perceptron newNeuron8 = new Perceptron(weights2);
  Perceptron newNeurons2[] = {newNeuron4, newNeuron5, newNeuron6, newNeuron7, newNeuron8};
  NeuronLayer newLayer2 = new NeuronLayer(newNeurons2);
  
  Perceptron newNeuron9 = new Perceptron(weights3);
  Perceptron newNeuron10 = new Perceptron(weights3);
  Perceptron newNeuron11 = new Perceptron(weights4);
  Perceptron newNeurons3[] = {newNeuron9, newNeuron10, newNeuron11};
  NeuronLayer newLayer3 = new NeuronLayer(newNeurons3);Neuron 
  NeuronLayer[] layers = {newLayer, newLayer2, newLayer3};
  net = new NeuralNet(layers); 500);
  net.calculateNetOutput(inputs);
}

void draw()
{
  background(backgroundColor);
  net.drawNeuralNet();
}


void drawLineTag(Perceptron neuron1, Perceptron neuron2)
{
  float xDifference = neuron2.coordinates[0] - neuron1.coordinates[0];
  float yDifference = neuron2.coordinates[1] - neuron1.coordinates[1];
  float theta = atan2(yDifference, xDifference);
  translate(neuron1.coordinates[0] + xDifference / 2.0, neuron1.coordinates[1] + yDifference / 2.0);
  rotate(theta);
  fill(textColor);
  textSize(8);
  String tag = "hi";
  text(tag,0,0);
  fill(Perceptron.perceptronColor);
  rotate(-theta);
  translate(-(neuron1.coordinates[0] + xDifference / 2.0), -(neuron1.coordinates[1] + yDifference / 2.0));
}

String calculateConnectionTag(Perceptron neuron1, Perceptron neuron2)
{
  float weightedInput = 0;
  return str(weightedInput); 
}