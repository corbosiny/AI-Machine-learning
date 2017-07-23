class Perceptron
{
  
 static final int size = 40;
 static final float defaultWeightRange = 10;
 static final int perceptronColor = 115;
 static final int textColor = 0;
 static final int textYAdjust = 4;
 static final int positiveTextXAdjust = 6;      
 static final int negativeTextXAdjust = 8;          //must account for the negative sign on text of negative numbers
 int coordinates[] = {0,0};
 float weights[];
 float currentOutput = 0;
 
 Perceptron(int numWeights)
 {
   this(numWeights, -defaultWeightRange, defaultWeightRange);
 }
 
 Perceptron(int numWeights, float minRange, float maxRange)
 {
   weights = new float[numWeights];
   for(int i = 0; i < numWeights; i++)
   {
     weights = (float[])append(weights, random(minRange, maxRange));
   }
 }
 
 
 Perceptron(float weights[])
 { 
   this.weights = new float[weights.length];
   arrayCopy(weights, this.weights);
 }
 
 float calculateOutput(float inputs[])
 {
   float sumOfWeightedInputs = calculateSigma(inputs);
   float output = activationFunction(sumOfWeightedInputs);
   currentOutput = output;
   return output;
 }
 
 float calculateSigma(float inputs[])
 {
   float sigma = 0;
   for(int inputNum = 0; inputNum < inputs.length; inputNum++)
   {
     sigma += inputs[inputNum] * weights[inputNum];
   }
   
   return sigma;
 }
 
 int activationFunction(float sigma)
 {
   if(sigma >= 0) {return 1;}
   else{return -1;}
 }
 
 void drawNeuron()
  {
     ellipse(coordinates[0], coordinates[1], size, size);
     fill(textColor);
     if(currentOutput < 0) {text(str(currentOutput), coordinates[0] - negativeTextXAdjust, coordinates[1] + textYAdjust);}
     else{text(str(currentOutput), coordinates[0] - positiveTextXAdjust, coordinates[1] + textYAdjust);}
     fill(Perceptron.perceptronColor);
  }
  
}