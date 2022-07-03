package com.example.prepoznavanjeautav2;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    //Inicijalizacija varijabli
    Button btEncode, btCapture;
    TextView txtMarka, txtModel, txtVjerojatnost;
    ImageView imageView;
    String sImage, stored_json, cImage, action;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Dodjeljivanje varijabli
        btEncode = findViewById(R.id.bt_encode);
        btCapture = findViewById(R.id.bt_capture);
        imageView = findViewById(R.id.image_view);
        txtMarka = findViewById(R.id.txtMarka);
        txtModel = findViewById(R.id.txtModel);
        txtVjerojatnost = findViewById(R.id.txtVjerojatnost);


        btEncode.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View view){
                action = "galerija";
                //Provjera uvjeta
                if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
                    //Kada dozvola nije dana, zatražimo je
                    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 100);
                }
                else if (ContextCompat.checkSelfPermission(MainActivity.this, Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                    ActivityCompat.requestPermissions(MainActivity.this, new String[]{Manifest.permission.CAMERA}, 100);
                }
                else {
                    //Kada je dozvola dana, pozivamo metodu
                    selectImage();
                }
            }
        });

        btCapture.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                action = "kamera";
                System.out.println("1111111111111111111111111111");
                //Otvaranje kamere
                Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(intent, 100);
            }
        });
    }
    ProgressDialog pd;
    private class JsonTask extends AsyncTask<String, String, String> {
        protected void onPreExecute() {
            super.onPreExecute();
            pd = new ProgressDialog(MainActivity.this);
            pd.setMessage("Please wait");
            pd.setCancelable(false);
            pd.show();
        }
        protected String doInBackground(String... params) {
            HttpURLConnection connection = null;
            BufferedReader reader = null;
            try {
                URL url = new URL(params[0]);
                connection = (HttpURLConnection) url.openConnection();
                connection.connect();
                InputStream stream = connection.getInputStream();
                reader = new BufferedReader(new InputStreamReader(stream));
                StringBuffer buffer = new StringBuffer();
                String line = "";
                while ((line = reader.readLine()) != null) {
                    buffer.append(line+"\n");
                    Log.d("Response: ", "> " + line);
                }return buffer.toString();
            } catch (MalformedURLException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                if (connection != null) {
                    connection.disconnect();
                }
                try {
                    if (reader != null) {
                        reader.close();
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
            return "";
        }
        @Override
        protected void onPostExecute(String result) {
            super.onPostExecute(result);
            if (pd.isShowing()){
                pd.dismiss();
            }
            try {
                stored_json = result;
                JSONObject json = new JSONObject(result);
                String marka = json.getString("marka");
                String model = json.getString("model");
                String vjerojatnost = json.getString("prob");
                txtMarka.setText("Marka: " + marka);
                txtModel.setText("Model: " + model);
                txtVjerojatnost.setText("Vjerojatnost " + vjerojatnost);
            } catch (JSONException e) {
                System.out.println(e);
            }
        }

    }

    private void selectImage() {
        //Brisanje prethodnih podataka
        imageView.setImageBitmap(null);
        //Inicijalizacija aktivnosti
        Intent intent = new Intent(Intent.ACTION_PICK);
        //Postavljanje tipa
        intent.setType("image/*");
        //Rezultat aktivnosti
        startActivityForResult(Intent.createChooser(intent, "Odaberi sliku"), 100);

    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        //Provjera uvjeta
        if (requestCode==100 && grantResults[0]==PackageManager.PERMISSION_GRANTED){
            //Kada je dozvola dana pozivamo metodu
            selectImage();
        }else{
            //Kada dozvola nije dana prikazuje se Toast
            Toast.makeText(getApplicationContext(), "Nemate dozvolu", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        //Provjera uvjeta
        if (requestCode==100 && resultCode==RESULT_OK && data!=null){
            //Kad je rezultat OK
            //Uri inicijalizacija
            Uri uri = data.getData();
            //Inicijalizacija bitmape
            try {
                if (action.equals("galerija")) {
                    //1. mogućnost - učitavanje iz galerije
                    Bitmap bitmap = MediaStore.Images.Media.getBitmap(getContentResolver(), uri);
                    //Inicijalizacija toka bajtova
                    ByteArrayOutputStream stream = new ByteArrayOutputStream();
                    //Komprimiranje bitmape
                    bitmap.compress(Bitmap.CompressFormat.JPEG, 100, stream);
                    //Inicijalizacija niza bajtova
                    byte[] bytes = stream.toByteArray();
                    //Dobivanje base64 kodiranog stringa
                    sImage = Base64.encodeToString(bytes, Base64.DEFAULT);

                    String custom_escaped_b64 = sImage.replace("/", "SLASH");
                    //System.out.println(custom_escaped_b64);
                    String URL = "http://3.87.42.223:8080/image/" + custom_escaped_b64;
                    new JsonTask().execute(URL);

                    //PRIKAZ SLIKE NA EKRANU
                    //Dekodiranje base64 stringa
                    byte[] byts = Base64.decode(sImage, Base64.DEFAULT);
                    //Inicijalizacija bitmape
                    Bitmap bitmapa = BitmapFactory.decodeByteArray(byts, 0, bytes.length);
                    //Bitmapa se postavlja na imageView
                    imageView.setImageBitmap(bitmapa);
                }
                else if (action.equals("kamera")) {
                    //2. mogućnost - slikanje:
                    Bitmap captureImage = (Bitmap) data.getExtras().get("data");
                    ByteArrayOutputStream stream = new ByteArrayOutputStream();
                    captureImage.compress(Bitmap.CompressFormat.JPEG, 100, stream);
                    byte[] bytes = stream.toByteArray();
                    cImage = Base64.encodeToString(bytes, Base64.DEFAULT);
                    String custom_escaped_b64 = cImage.replace("/", "SLASH");
                    String URL = "http://3.87.42.223:8080/image/" + custom_escaped_b64;
                    new JsonTask().execute(URL);
                    byte[] byts = Base64.decode(cImage, Base64.DEFAULT);
                    Bitmap bitmapa = BitmapFactory.decodeByteArray(byts, 0, bytes.length);
                    imageView.setImageBitmap(captureImage);
                }
                else{
                    System.out.println("Radnja ne postoji.");
                }

            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(getApplicationContext(), "Doslo je do greske...", Toast.LENGTH_SHORT).show();
            }
        }
    }
}