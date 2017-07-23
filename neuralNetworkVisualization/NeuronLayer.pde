class NeuronLayer
{
  
  Perceptron neurons[] = new Perceptron[0];
  
   NeuronLayer(float weights[][])
   {
      for(int i = 0; i < weights.length; i++)
      {
        Perceptron newNeuron = new Perceptron(weights[i]);
        neurons = (Perceptron[])append(neurons, newNeuron);
      }
   }

  NeuronLayer(int numNeurons, int numWeights)
  {
   this(numNeurons, numWeights, -Perceptron.defaultWeightRange, Perceptron.defaultWeightRange);
  }
  
  NeuronLayer(int numNeurons, int numWeights, float minWeightRange, float maxWeightRange)
  {
    for(int i = 0; i < numNeurons; i++)
    {
      Perceptron newNeuron = new Perceptron(numWeights, minWeightRange, maxWeightRange);
      neurons = (Perceptron[])append(neurons, newNeuron); 
    }
  }
  
   NeuronLayer(Perceptron neurons[])
   {
      this.neurons = new Perceptron[neurons.length];
      arrayCopy(neurons, this.neurons);
   }
 
   float []calculateOutputArray(float inputs[][])
   {
     float outputs[] = new float[neurons.length];
     for(int numNeuron = 0; numNeuron < neurons.length; numNeuron++)
     {
         outputs[numNeuron] = neurons[numNeuron].calculateOutput(inputs[numNeuron]);
     }
     return outputs;
   }
   
  void drawNeuronLayer()
  {
    for(Perceptron neuron: neurons)
    {
      neuron.drawNeuron();
    }
  }

}