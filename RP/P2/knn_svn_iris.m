%% Cargar el conjunto de datos Iris
load fisheriris
X = meas;           % Características de las flores (150x4)
Y = species;        % Etiquetas de las especies (150x1)

%% Convertir etiquetas a valores numéricos
[Y_num, etiquetas] = grp2idx(Y);  % Convierte las etiquetas a 1, 2, 3

%% Dividir en conjunto de entrenamiento y prueba (70% - 30%)
rng('default');  % Para reproducibilidad
cv = cvpartition(Y_num, 'HoldOut', 0.3);
XTrain = X(cv.training,:);
YTrain = Y_num(cv.training);
XTest = X(cv.test,:);
YTest = Y_num(cv.test);

%% Entrenar y evaluar KNN
knnModel = fitcknn(XTrain, YTrain,...
    'NumNeighbors', 5,...
    'Distance', 'euclidean',...
    'Standardize', true);

knnPred = predict(knnModel, XTest);
accuracyKNN = sum(knnPred == YTest)/numel(YTest);

%% Entrenar y evaluar SVM
% Crear plantilla SVM con kernel lineal
template = templateSVM(...
    'Standardize', true,...
    'KernelFunction', 'linear',...
    'BoxConstraint', 1);

svmModel = fitcecoc(XTrain, YTrain,...
    'Learners', template,...
    'Coding', 'onevsall');

svmPred = predict(svmModel, XTest);
accuracySVM = sum(svmPred == YTest)/numel(YTest);

%% Mostrar resultados
fprintf('Exactitud KNN: %.2f%%\n', accuracyKNN*100);
fprintf('Exactitud SVM: %.2f%%\n', accuracySVM*100);

%% Visualizar matrices de confusión
figure
confusionchart(YTest, knnPred,...
    'RowSummary', 'row-normalized',...
    'ColumnSummary', 'column-normalized',...
    'Title', 'Matriz de Confusión - KNN');

figure
confusionchart(YTest, svmPred,...
    'RowSummary', 'row-normalized',...
    'ColumnSummary', 'column-normalized',...
    'Title', 'Matriz de Confusión - SVM');