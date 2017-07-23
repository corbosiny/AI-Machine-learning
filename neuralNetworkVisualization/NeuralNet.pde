class NeuralNet
{
  
   NeuronLayer layers[];

   NeuralNet(int numLayers, int numNeurons[], int numWeights)
   {
     layers = new NeuronLayer[numLayers];
     layers[0] = new NeuronLayer(numNeurons[0], numWeights);
     for(int layerNum = 1; layerNum < numLayers; layerNum++)
     {
       layers[layerNum] = new NeuronLayer(numNeurons[layerNum], layers[layerNum - 1].neurons.length); 
     }
   }
   
   NeuralNet(NeuronLayer layers[])
   {
     this.layers = new NeuronLayer[layers.length];
     arrayCopy(layers, this.layers);
     calculateLayerCoordinates();
   }
  
   float[] calculateNetOutput(float inputs[][])
   {
      
     float outputs[] = layers[0].calculateOutputArray(inputs);
     print("START");
     println(outputs);
     for(int layerNum = 1; layerNum < layers.length; layerNum++)
     {
       float nextInputs[][] = formatOutputsToNextInputs(outputs, layerNum);
       print("Length: ");
       print(str(nextInputs.length) + " ");
       println(str(nextInputs[0].length));
       outputs = layers[layerNum].calculateOutputArray(nextInputs);
       println(outputs);
     }
    return outputs; 
   }
  
  
  float [][]formatOutputsToNextInputs(float outputs[], int layerNum)
  {
    float newInputs[][] = new float[layers[layerNum].neurons.length][];
    for(int i = 0; i < layers[layerNum].neurons.length; i++)
    {
      newInputs[i] = new float[outputs.length];
      arrayCopy(outputs, newInputs[i]);
    }
    return newInputs;
  }
 
 
  void calculateLayerCoordinates()
  {
     for(int layerNum = 0; layerNum < layers.length; layerNum++)
     {
       NeuronLayer layer = layers[layerNum];
     
       for(int neuronNum = 0; neuronNum < layer.neurons.length; neuronNum++)
       {
         int coordinates[] = new int[2];
         coordinates[0] = (layerNum + 1) * 100;
         coordinates[1] = (int)(75 + 450 * (float)((neuronNum + 1) / (layer.neurons.length + 1.0)));       
         arrayCopy(coordinates, layer.neurons[neuronNum].coordinates);
       }
     }
  }
  
  void drawNeuralNet()
  {
     drawNeuronConnections(); 
     for(NeuronLayer layer: layers)
     {
       layer.drawNeuronLayer();
     }   
  }
 
 void drawNeuronConnections()
  {
    for(int layerNum = 0; layerNum < layers.length - 1; layerNum++)
    {
      drawNeuronConnectionBetweenLayers(layerNum, layerNum + 1);
    }
  }

  void drawNeuronConnectionBetweenLayers(int currentLayerNum, int nextLayerNum)
  {
     NeuronLayer currentLayer = layers[currentLayerNum];
     NeuronLayer nextLayer = layers[nextLayerNum];
     for(int i = 0; i < currentLayer.neurons.length; i++)
     {
       for(int j = 0; j < nextLayer.neurons.length; j++)
       {
         drawNeuronConnection(currentLayer.neurons[i], nextLayer.neurons[j]);
       }
     }
  }

  void drawNeuronConnection(Perceptron neuron1, Perceptron neuron2)
 {
  line(neuron1.coordinates[0], neuron1.coordinates[1], neuron2.coordinates[0], neuron2.coordinates[1]);
  drawLineTag(neuron1, neuron2);
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
  
}